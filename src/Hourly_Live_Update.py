## IMPORTS
import time, os, requests, threading
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from google.cloud import storage
import concurrent.futures
import urllib.request
from io import StringIO

# FUNCTIONS
def create_airqual_dict(city, city_name, state):
    """Return dictionary of airqual results by City."""
    city_live_dict = {}
    local_dt = city['data']['time']['s']
    try: local_date = datetime.strptime(local_dt, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    except: local_date = None
    try: local_time = datetime.strptime(local_dt, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
    except: local_time = None
    city_live_dict['local_date_airqual'] = local_date
    city_live_dict['local_time_airqual'] = local_time
    
    UTC_dt = city['data']['time']['s']
    UTC_timezone = city['data']['time']['tz']
    UTC_timezone = int(datetime.strptime(UTC_timezone, '-%H:%M').strftime('%H'))
    UTC_dt_adjusted = datetime.strptime(UTC_dt, '%Y-%m-%d %H:%M:%S') + timedelta(hours=UTC_timezone)
    try: UTC_date = datetime.strptime(str(UTC_dt_adjusted), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    except: UTC_date = None
    try: UTC_time = datetime.strptime(str(UTC_dt_adjusted), '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
    except: UTC_time = None
    city_live_dict['UTC_date'] = UTC_date
    city_live_dict['UTC_time'] = UTC_time
    
    
    try: city_live_dict['city'] = city_name #city['data']['city']['name']
    except: city_live_dict['city']= None
    try: city_live_dict['state'] = state
    except: city_live_dict['state']= None
    try: city_live_dict['full_time'] = city['data']['time']['s']
    except: city_live_dict['full_time'] = None
    try: city_live_dict['time zone'] = city['data']['time']['tz']
    except: city_live_dict['time zone'] = None
    try: city_live_dict['second'] = city['data']['time']['v']
    except: city_live_dict['second'] = None
    try: city_live_dict['lat_airqual'] = city['data']['city']['geo'][0]
    except: city_live_dict['lat_airqual'] = None
    try: city_live_dict['long_airqual'] = city['data']['city']['geo'][1]
    except: city_live_dict['long_airqual'] = None
    try: city_live_dict['aqi'] = city['data']['aqi']
    except: city_live_dict['aqi'] = None
    try: city_live_dict['pm2.5'] = city['data']['iaqi']['pm25']['v']
    except: city_live_dict['pm2.5'] = None
    try: city_live_dict['co'] = city['data']['iaqi']['co']['v']
    except: city_live_dict['co'] = None
    try: city_live_dict['no2'] = city['data']['iaqi']['no2']['v']
    except: city_live_dict['no2'] = None
    try: city_live_dict['o3'] = city['data']['iaqi']['o3']['v']
    except: city_live_dict['o3'] = None
    try: city_live_dict['humidity_airqual'] = city['data']['iaqi']['h']['v']
    except: city_live_dict['humidity_airqual'] = None
    try: city_live_dict['pressure_airqual'] = city['data']['iaqi']['p']['v']
    except: city_live_dict['pressure_airqual'] = None
    
    return city_live_dict


def create_weather_dict(data, state):
    data_dict = {}
    
    local_dt = data['dt'] + data['timezone']
    try: local_date = datetime.utcfromtimestamp(local_dt).strftime('%Y-%m-%d')
    except: local_date = None
    try: local_time = datetime.utcfromtimestamp(local_dt).strftime('%H:00')
    except: local_time = None
    data_dict['local_date_weather'] = local_date
    data_dict['local_time_weather'] = local_time
    UTC_dt = data['dt']
    try: UTC_date = datetime.utcfromtimestamp(UTC_dt).strftime('%Y-%m-%d')
    except: UTC_date = None
    try: UTC_time = datetime.utcfromtimestamp(UTC_dt).strftime('%H:00')
    except: UTC_time = None
    data_dict['UTC_date'] = UTC_date
    data_dict['UTC_time'] = UTC_time

    # (K − 273.15) × 9/5 + 32 #Kelvin to F
    try: data_dict['city'] = data['name']
    except: data_dict['city'] = None
    try: data_dict['state'] = state
    except: data_dict['state'] = None
    try: data_dict['long_weather'] = data['coord']['lon']
    except: data_dict['long_weather'] = None
    try: data_dict['lat_weather'] = data['coord']['lat']
    except: data_dict['lat_weather'] = None
    try: data_dict['weather_id'] = data['weather'][0]['id']
    except: data_dict['weather_id'] = None
    try: data_dict['weather_clouds'] = data['weather']['clouds']
    except: data_dict['weather_clouds'] = None
    try: data_dict['weather_main'] = data['weather'][0]['main']
    except: data_dict['weather_main'] = None
    try: data_dict['weather_description'] = data['weather'][0]['description']
    except: data_dict['weather_description'] = None
    try: data_dict['temp'] = round((data['main']['temp'] - 273.15) * 9/5 + 32, 2) #Kelvin to F
    except: data_dict['temp'] = None
    try: data_dict['feels_like'] = round((data['main']['feels_like'] - 273.15) * (9/5) + 32, 2) #Kelvin to F
    except: data_dict['feels_like'] = None
    try: data_dict['temp_min'] = round((data['main']['temp_min'] - 273.15) * (9/5) + 32, 2) #Kelvin to F
    except: data_dict['temp_min'] = None
    try: data_dict['temp_max'] = round((data['main']['temp_max'] - 273.15) * (9/5) + 32, 2) #Kelvin to F
    except: data_dict['temp_max'] = None
    try: data_dict['pressure_weather'] = data['main']['pressure']
    except: data_dict['pressure_weather'] = None
    try: data_dict['humidity_weather'] = data['main']['humidity']
    except: data_dict['humidity_weather'] = None
    try: data_dict['visibility'] = data['visibility']
    except: data_dict['visibility'] = None
    try: data_dict['wind_speed'] = data['wind']['speed']
    except: data_dict['wind_speed'] = None
    try: data_dict['wind_deg'] = data['wind']['deg']
    except: data_dict['wind_deg'] = None
    try: data_dict['wind_gust'] = data['wind']['gust']
    except: data_dict['wind_gust'] = None
    
    sunrise_time = data['sys']['sunrise'] + data['timezone']
    sunset_time = data['sys']['sunset'] + data['timezone']
    try: data_dict['sunrise'] = datetime.utcfromtimestamp(sunrise_time).strftime('%H:%M:%S')
    except: data_dict['sunrise'] = None
    try: data_dict['sunset'] = datetime.utcfromtimestamp(sunset_time).strftime('%H:%M:%S')
    except: data_dict['sunset'] = None
    
    return data_dict


def getList(dict):
    return dict.keys()

## LOAD THE AIRQUAL & WEATHER DATA PER STATE

def create_csv():
    # STATE DATA

    Capitals_dict = {"Alabama": {"City": "Montgomery", "Weather_Code": 4076784, "Airqual_Code": 7379}, "Alaska": {"City": "Juneau", "Weather_Code": 5554072, "Airqual_Code": 7610}, "Arizona": {"City": "Phoenix", "Weather_Code": 5308655, "Airqual_Code": 5944}, "Arkansas": {"City": "Little Rock", "Weather_Code": 4119403, "Airqual_Code": 7383}, "California": {"City": "Sacramento", "Weather_Code": 5389489, "Airqual_Code": 303}, "Colorado": {"City": "Denver", "Weather_Code": 5419384, "Airqual_Code": 6314}, "Connecticut": {"City": "Hartford", "Weather_Code": 4835797, "Airqual_Code": 7387}, "Delaware": {"City": "Dover", "Weather_Code": 4142290, "Airqual_Code": 7392}, "Florida": {"City": "Tallahassee", "Weather_Code": 4174715, "Airqual_Code": 6295}, "Georgia": {"City": "Atlanta", "Weather_Code": 4180439, "Airqual_Code": 13288}, "Hawaii": {"City": "Honolulu", "Weather_Code": 5856195, "Airqual_Code": 5273}, "Idaho": {"City": "Boise", "Weather_Code": 5586437, "Airqual_Code": 9615}, "Illinois": {"City": "Springfield", "Weather_Code": 4250542, "Airqual_Code": 9641}, "Indiana": {"City": "Indianapolis", "Weather_Code": 4259418, "Airqual_Code": 8699}, "Iowa": {"City": "Des Moines", "Weather_Code": 4853828, "Airqual_Code": 6924}, "Kansas": {"City": "Topeka", "Weather_Code": 4280539, "Airqual_Code": 9514}, "Kentucky": {"City": "Frankfort", "Weather_Code": 4292188, "Airqual_Code": 7330}, "Louisiana": {"City": "Baton Rouge", "Weather_Code": 4315588, "Airqual_Code": 12846}, "Maine": {"City": "Augusta", "Weather_Code": 4957003, "Airqual_Code": 7640}, "Maryland": {"City": "Annapolis", "Weather_Code": 4347242, "Airqual_Code": 7418}, "Massachusetts": {"City": "Boston", "Weather_Code": 4930956, "Airqual_Code": 5883}, "Michigan": {"City": "Lansing", "Weather_Code": 4998830, "Airqual_Code": 13070}, "Minnesota": {"City": "Saint Paul", "Weather_Code": 5045360, "Airqual_Code": 7348}, "Mississippi": {"City": "Jackson", "Weather_Code": 4431410, "Airqual_Code": 7432}, "Missouri": {"City": "Jefferson City", "Weather_Code": 4392388, "Airqual_Code": 7353}, "Montana": {"City": "Helena", "Weather_Code": 5656882, "Airqual_Code": 7523}, "Nebraska": {"City": "Lincoln", "Weather_Code": 5072006, "Airqual_Code": 7364}, "Nevada": {"City": "Carson City", "Weather_Code": 5501344, "Airqual_Code": 8350}, "New Hampshire": {"City": "Concord", "Weather_Code": 5084868, "Airqual_Code": 7449}, "New Jersey": {"City": "Trenton", "Weather_Code": 5105496, "Airqual_Code": 8530}, "New Mexico": {"City": "Santa Fe", "Weather_Code": 5490263, "Airqual_Code": 6281}, "New York": {"City": "Albany", "Weather_Code": 5106834, "Airqual_Code": 5100}, "North Carolina": {"City": "Raleigh", "Weather_Code": 4487042, "Airqual_Code": 7668}, "North Dakota": {"City": "Bismarck", "Weather_Code": 5688025, "Airqual_Code": 7445}, "Ohio": {"City": "Columbus", "Weather_Code": 4509177, "Airqual_Code": 7591}, "Oklahoma": {"City": "Oklahoma City", "Weather_Code": 4544349, "Airqual_Code": 10178}, "Oregon": {"City": "Salem", "Weather_Code": 5750162, "Airqual_Code": 89}, "Pennsylvania": {"City": "Harrisburg", "Weather_Code": 5192726, "Airqual_Code": 6423}, "Rhode Island": {"City": "Providence", "Weather_Code": 5224151, "Airqual_Code": 7478}, "South Carolina": {"City": "Columbia", "Weather_Code": 4575352, "Airqual_Code": 9515}, "South Dakota": {"City": "Pierre", "Weather_Code": 5767918, "Airqual_Code": 8359}, "Tennessee": {"City": "Nashville", "Weather_Code": 4644585, "Airqual_Code": 7496}, "Texas": {"City": "Austin", "Weather_Code": 4671654, "Airqual_Code": 224}, "Utah": {"City": "Salt Lake City", "Weather_Code": 5780993, "Airqual_Code": 12862}, "Vermont": {"City": "Montpelier", "Weather_Code": 5238685, "Airqual_Code": 7376}, "Virginia": {"City": "Richmond", "Weather_Code": 4781708, "Airqual_Code": 5357}, "Washington": {"City": "Olympia", "Weather_Code": 5805687, "Airqual_Code": 115}, "West Virginia": {"City": "Charleston", "Weather_Code": 4801859, "Airqual_Code": 9524}, "Wisconsin": {"City": "Madison", "Weather_Code": 5261457, "Airqual_Code": 10175}, "Wyoming": {"City": "Cheyenne", "Weather_Code": 5821086, "Airqual_Code": 9526}}
    
    list_states = getList(Capitals_dict)

    results = pd.DataFrame()

    for i in list_states:
        state_weather = Capitals_dict[i]['Weather_Code'] #Capitals_dict[i]['Weather_Code']
        state_airqual = Capitals_dict[i]['Airqual_Code'] #Capitals_dict[i]['Airqual_Code']
        weather_url = 'https://api.openweathermap.org/data/2.5/weather?id={}&appid=677381a374af2b031a7213a9531c9711'.format(state_weather)
        airqual_url = 'https://api.waqi.info/feed/@{}/?token=1fd4e786510e90210e6604b26f130f8dd2f53478'.format(state_airqual)

        weather_response = requests.get(weather_url)
        airqual_response = requests.get(airqual_url)

        weather_data = weather_response.json()
        airqual_data = airqual_response.json()

        ## CONVERT TO DICT
        weather_dict = {}
        weather_dict[0] = create_weather_dict(weather_data, i)
        weather_df = pd.DataFrame.from_dict(weather_dict, orient='index')
        
        airqual_dict = {}
        airqual_dict[1] = create_airqual_dict(airqual_data, Capitals_dict[i]['City'], i)
        airqual_df = pd.DataFrame.from_dict(airqual_dict, orient='index')
    
        # MERGE WEATHER AND AIRQUAL
        weather_airqual_df = pd.merge(airqual_df, weather_df, on=['city','state','UTC_date','UTC_time'], how='outer')

        # MERGE TO MASTER DF
        results = pd.concat([results, weather_airqual_df])

    # VERIFY UTC UP TO DATE

    utc_hour_now = datetime.utcnow().strftime("%H:00") 
    results = results[results['UTC_time'] == utc_hour_now]
    results = results[['UTC_date', 'UTC_time', 'city', 'state','local_date_airqual', 'local_time_airqual', 'local_date_weather', 'local_time_weather',
        'full_time', 'time zone', 'second', 'lat_airqual', 'long_airqual', 'aqi', 'pm2.5', 'co', 'no2', 'o3', 'humidity_airqual',
       'pressure_airqual', 'long_weather', 'lat_weather', 'weather_id', 'weather_clouds', 'weather_main', 'weather_description', 'temp', 'feels_like', 'temp_min',
       'temp_max', 'pressure_weather', 'humidity_weather', 'visibility','wind_speed', 'wind_deg', 'wind_gust', 'sunrise', 'sunset']]
    
    ## PULL PAST DATA

    previous_live_df = pd.read_csv('gs://project-1050-data/live.csv')

    ## CONCAT PREVIOUS LIVE & NEW LIVE

    final_data = pd.concat([previous_live_df, results])
    print(final_data.columns)
    return final_data #remove

    # SEND DATA TO BUCKET

#     f = StringIO()
#     gcs = storage.Client()
#     final_data.to_csv(f, index=False)
#     f.seek(0)

#     gcs.bucket('project-1050-data').blob('live.csv').upload_from_file(f, content_type='text/csv')

print(create_csv())
