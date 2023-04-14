import requests
import json
import datetime

url = "https://www.cineworld.co.uk/uk/data-api-service/v1/quickbook/10108/film-events/in-cinema/019/at-date/2023-04-14?attr=&lang=en_GB"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
json_dict = response.json()
films = json_dict["body"]["films"]

allowed_attribute_ids = {"u", "pg", "12", "12a", "15", "18"}

for film in films:
    for attr_id in film["attributeIds"]:
        if attr_id in allowed_attribute_ids:
            print(film["name"], attr_id)
            break
