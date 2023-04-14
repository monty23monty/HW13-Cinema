import requests
from bs4 import BeautifulSoup
import datetime

url = "https://www.cineworld.co.uk/uk/data-api-service/v1/quickbook/10108/film-events/in-cinema/019/at-date/2023-04-10?attr=&lang=en_GB"
response = requests.get(url)
print(response.content)
