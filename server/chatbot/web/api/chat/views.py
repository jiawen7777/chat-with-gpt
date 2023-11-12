import json

from fastapi import APIRouter
from starlette.responses import StreamingResponse
import openai
from chatbot.web.api.chat.schema import RequestModel


router = APIRouter()



with open("api_key.txt", 'r') as file:
    openai.api_key = file.read().strip()


def get_openai_generator(request_message: RequestModel):
    openai_stream = openai.ChatCompletion.create(
        model=request_message.model,
        messages=request_message.messages,
        temperature=request_message.temperature,
        stream=True,
    )
    result_dict = dict()
    for event in openai_stream:
        if "content" in event["choices"][0].delta:
            current_response = event["choices"][0].delta.content
            # result_dict["data"] = current_response
            yield "data: " + current_response + "\n\n"


def get_openai_generator2(request_message: RequestModel):
    openai_stream = openai.ChatCompletion.create(
        model=request_message.model,
        messages=request_message.messages,
        temperature=request_message.temperature,
        stream=True,
    )
    for event in openai_stream:
        yield event

@router.post('/stream')
async def stream(request: RequestModel):
    return StreamingResponse(get_openai_generator(request),
                             media_type='text/event-stream')
