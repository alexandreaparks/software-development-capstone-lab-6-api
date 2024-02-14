import requests
from pprint import pprint
import os


key = os.environ.get('WEATHER_KEY')  # returns None if it doesn't exist
print(key)

url = 'https://api.openweathermap.org/data/2.5/weather'  # removed everything after ? for query params

city = input('Enter city: ')
state = input('Enter the 2-letter abbreviated state name: ')

location = f'{city},{state},us'

query = {'q': location, 'units': 'imperial', 'appid': key}

data = requests.get(url, params=query).json()  # uses query parameters
pprint(data)

current_temperature = data['main']['temp']
print(f'The current temperature is {current_temperature}F')