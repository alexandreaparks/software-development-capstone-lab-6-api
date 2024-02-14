import logging
import requests
import os
from datetime import datetime

"""
Alexandrea Parks
2/14/2024
forecast.py
This program works with a Weather API and requests a 3-hour, 5-day weather forecast for a user given location.

The program either prints the forecast, or a user-friendly message saying the forecast could not be retrieved.
All other messages are logged to the dubug.log file.
"""

logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
url = 'http://api.openweathermap.org/data/2.5/forecast'
key = os.environ.get('WEATHER_KEY')  # returns None if it doesn't exist


def main():
    location = get_location()
    weather_data, error = get_weather_data(location, key)
    if error:  # if error is not None
        print('Sorry, could not get the weather forecast')
    else:
        get_forecast(weather_data)


def get_location():
    """
    Gets location from user input and returns location formatted like city,country
    """
    city, country = '', ''
    while len(city) == 0:
        city = input('Enter the name of the city: ').strip()

    while len(country) != 2:
        country = input('Enter the 2-letter country code: ').strip()

    location = f'{city},{country}'
    return location


def get_weather_data(location, key):
    """
    Makes request to API and returns a tuple with the weather data and the value None.
    If an exception is raised, it returns the value None and the error message.
    """
    try:
        query = {'q': location, 'units': 'imperial', 'appid': key}
        response = requests.get(url, params=query)
        response.raise_for_status()  # raises exception for error
        data = response.json()
        return data, None
    except Exception as e:
        logging.exception(f'Error requesting URL {url}')
        return None, e  # return tuple with error


def get_forecast(weather_data):
    """
    Loops through list of forecasts, accesses the date and time, temperature, description,
    and wind speed, then prints data for 3 hour increments in a 5-day forecast.
    """
    try:
        list_of_forecasts = weather_data['list']
        for forecast in list_of_forecasts:

            temp = forecast['main']['temp']
            timestamp = forecast['dt']
            forecast_date = datetime.fromtimestamp(timestamp)  # converts to local datetime
            description = forecast['weather'][0]['description']  # weather's value is a list - access index 0
            wind_speed = forecast['wind']['speed']

            print(f'Forecast date: {forecast_date} Temperature: {temp}F '
            f'Description: {description} Wind Speed: {wind_speed} MPH\n')
    except KeyError:  # handles error if JSON is not in expected format
        print('Sorry, could not get the weather forecast')
        logging.exception('Error reading JSON data')


if __name__ == '__main__':
    main()






