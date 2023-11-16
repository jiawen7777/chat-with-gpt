import requests
import json

api_key = ""
api_url = "https://restapi.amap.com/v3/weather/weatherInfo?city="
loc_dict = {
    'Central and Western': 810001,
    'Wan Chai': 810002,
    'Eastern': 810003,
    'Southern': 810004,
    'Yau Tsim Mong': 810005,
    'Sham Shui Po': 810006,
    'Kowloon City': 810007,
    'Wong Tai Sin': 810008,
    'Kwun Tong': 810009,
    'Tsuen Wan': 810010,
    'Tuen Mun': 810011,
    'Yuen Long': 810012,
    'North': 810013,
    'Tai Po': 810014,
    'Sai Kung': 810015,
    'Sha Tin': 810016,
    'Kwai Tsing': 810017,
    'Outlying Islands': 810018,
    'Nossa Senhora de Fatima Parish': 820001,
    'Santo Antonio Parish': 820002,
    'San Lazaro Parish': 820003,
    'Sé Parish': 820004,
    'São Lourenço Parish': 820005,
    'Taipa and Coloane Parish': 820006,
    'Cotai Strip': 820007,
    'St. Francis Xavier\'s Parish': 820008
}


def get_weather(city_name: str):
    city_code = loc_dict.get(city_name, -1)
    req_url = api_url + str(city_code) + "&key=" + api_key
    response = requests.get(req_url)
    response_content = response.content
    content_str = response_content.decode('utf-8')  # Decode the bytes into a string
    response_dict = json.loads(content_str)  # Parse the string into a dictionary
    live_data = response_dict['lives']
    if len(live_data) == 0 or len(live_data[0]) == 0:
        return dict()

    else:
        tem_data = response_dict['lives'][0]
        result_dict = {
            "temperature": tem_data['temperature'],
            "wind_direction": tem_data['winddirection'],
            "humidity": tem_data['humidity'],
            "report_time": tem_data['reporttime']
        }
        return json.dumps(result_dict)


