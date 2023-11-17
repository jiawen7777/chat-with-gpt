import json

from fastapi import APIRouter
from starlette.responses import StreamingResponse
import openai
from chatbot.web.api.chat.schema import RequestModel
from chatbot.web.api.chat.algorithms import weather_util
import time
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()


def get_openai_generator(request_message: RequestModel):
    start_time = time.time()
    openai_stream = openai.ChatCompletion.create(
        model=request_message.model,
        messages=request_message.messages,
        temperature=request_message.temperature,
        stream=True,
    )
    end_time = time.time()
    print("non-Function Calling time cost:", end_time - start_time)

    for event in openai_stream:
        if "content" in event["choices"][0].delta:
            current_response = event["choices"][0].delta.content
            # result_dict["data"] = current_response
            yield "data: " + current_response + "\n\n"


functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location, including"
                       " temperature, wind_direction, humidity and report_time",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }]


def get_openai_generator_function_calling(request_message: RequestModel):
    start_time = time.time()
    openai_stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=request_message.messages,
        temperature=request_message.temperature,
        stream=True,
        functions=functions,
        function_call="auto"  # auto is default, but we'll be explicit
    )
    function_call_str = ""
    function_call_name = ""
    function_call_flag = False
    end_time = time.time()
    print("Function Calling time cost:", end_time - start_time)
    for event in openai_stream:
        # the end of function call state, this is the last event of the request,
        # after this event, the request will be closed.
        if (event["choices"][0]["finish_reason"] is not None
            and event["choices"][0]["finish_reason"] == "function_call"):
            function_call_flag = False
            # call function by using function_call_name
            my_dict = json.loads(function_call_str)

            # 提取 location 值
            location = my_dict["location"]
            function_call_response = None
            if function_call_name == "get_current_weather":
                function_call_response = weather_util.get_weather(city_name=location)
            if len(function_call_response) == 0:
                yield "data: " + f"Currently no weather information for {location}" + "\n\n"
                continue

            appended_message = request_message.messages
            appended_message = appended_message + [{
                "role": "function",
                "name": "get_current_weather",
                "content": function_call_response,
            }]
            print(appended_message)
            function_call_stream = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=appended_message,
                temperature=request_message.temperature,
                stream=True
            )
            for stream_event in function_call_stream:
                if "content" in stream_event["choices"][0].delta:
                    current_response = stream_event["choices"][0].delta.content
                    # result_dict["data"] = current_response
                    yield "data: " + current_response + "\n\n"
            continue

        # get delta
        delta = event["choices"][0].delta

        # during the function call flag
        if function_call_flag:
            function_call_str += delta["function_call"]["arguments"]
            continue
        # collecting information of function calling
        if "function_call" in delta:
            # start function_call mode
            function_call_flag = True
            function_call_name = delta["function_call"]["name"]
            continue

        #  non-functional calling
        if "content" in event["choices"][0].delta:
            current_response = event["choices"][0].delta.content
            # result_dict["data"] = current_response
            yield "data: " + current_response + "\n\n"


def get_current_weather(location: str, unit: str = "celsius"):
    weather_info = {
        "location": location,
        "temperature": "27",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


@router.post('/stream')
async def stream(request: RequestModel):
    if request.function_calling:
        return StreamingResponse(get_openai_generator_function_calling(request),
                                 media_type='text/event-stream')
    return StreamingResponse(get_openai_generator(request),
                             media_type='text/event-stream')
