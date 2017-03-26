import numpy as np
import requests
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


def historical_weather(address, start_date, end_date, units='e'):
    """
    Input: address, start date, end date and units (strings)
    Output: historical weather data (json)
    Date format: 2017-03-25 -> '20170325'
    """
    # Get credentials from .env
    USERNAME = os.environ.get("WEATHER_USERNAME")
    PASSWORD = os.environ.get("WEATHER_PASSWORD")
    API_KEY = os.environ.get("API_KEY")
    # Get latude and longitude coordinates for given address
    payload = {'query': address,
               'locationType': 'address',
               'language': 'en-US'}
    r = requests.get('https://' +
                     USERNAME + ':' + PASSWORD +
                     '@twcservice.mybluemix.net/api/weather/v3/location/search',
                     params=payload)
    lat = r.json()['location']['latitude'][0]
    lon = r.json()['location']['longitude'][0]
    # Get 7 day forcast from latude and longitude coordinates
    payload = {'units': 'e',
               'startDate': start_date,
               'endDate': end_date}
    r = requests.get('http://api.weather.com/v1/geocode/' +
                     str(lat) + '/' + str(lon) +
                     '/observations/historical.json?apiKey=' +
                     API_KEY, params=payload)
    return r.json()


def forecast_weather(address, units='e'):
    """
    Input: address and units (strings)
    Output: 7 day weather forecast (json)
    Date format: 2017-03-25 -> '20170325'
    """
    # Get credentials from .env
    USERNAME = os.environ.get("WEATHER_USERNAME")
    PASSWORD = os.environ.get("WEATHER_PASSWORD")
    # Get latude and longitude coordinates for given address
    payload = {'query': address, 'locationType': 'address', 'language': 'en-US'}
    r = requests.get('https://' +
                     USERNAME + ':' + PASSWORD +
                     '@twcservice.mybluemix.net/api/weather/v3/location/search',
                     params=payload)
    lat = r.json()['location']['latitude'][0]
    lon = r.json()['location']['longitude'][0]
    # Get 7 day forcast from latude and longitude coordinates
    payload = {'units': units}
    r = requests.get('https://' +
                     USERNAME + ':' + PASSWORD +
                     '@twcservice.mybluemix.net/api/weather/v1/geocode/' +
                     str(lat) + '/' + str(lon) +
                     '/forecast/daily/7day.json',
                     params=payload)
    return r.json()


def historical_gloom(hist_json):
    """
    Input: historical weather information (json)
    Output: bad weather score (float)
    """
    mean_clouds = []
    mean_precip = []
    # count instances of overcast skies and precipitation
    for ob in hist_json['observations']:
        if ob['clds'] == 'OVC':
            mean_clouds.append(1)
        else:
            mean_clouds.append(0)
        if type(ob['precip_hrly']) == float and ob['precip_hrly'] > 0:
            mean_precip.append(1)
        else:
            mean_precip.append(0)
    # find gloom score and scale from 0 to 1
    return (np.mean(mean_clouds) + (2 * np.mean(mean_precip))) / 3


def outdoor_bool(forecast_json):
    """
    Input: 7 day weather forecast (json)
    Output: outside activity bool (int)
    """
    # get forecast for next day
    forecast = forecast_json['forecasts'][1]['day']
    # return bool for low prop precip and comfortable windchill
    return forecast['pop'] <= 0.2 and forecast['wc'] >= 40
