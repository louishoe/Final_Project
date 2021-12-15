
def import_data():
    
    import pandas as pd
    import numpy as np
    #from datetime import date, timedelta, datetime
    import datetime as dt

    today = dt.date.today()
    now = dt.datetime.today()

    # Bring in the live data that refresehes every hour on the 50th minute that captures the current floored hour:
    live = pd.read_csv('https://storage.googleapis.com/project-1050-data/live.csv')
    # Bring in the state abbreviations for the map graph: 
    st_codes = pd.read_csv('https://storage.googleapis.com/project-1050-data/state_codes.csv')
    live = live.join(st_codes.set_index('State'), on="state")
    live.rename(columns={"temp":"Temperature", "Alpha code":"STATE"}, inplace=True)

    # Adjust the time across 
    live['graph_date'] = live['UTC_date'] + ' '  + live['UTC_time']
    live['UTC_date'] = pd.to_datetime(live['UTC_date']).dt.date
    dtm = today - dt.timedelta(1)
    dtm = dt.datetime.strptime(str(dtm), '%Y-%m-%d').date()
    live = live[(live['UTC_date']>= dtm)]

    # Bring in historical AQI data:
    historic = pd.read_csv('https://storage.googleapis.com/project-1050-data/2021_AQI_hist.csv')
    historic['date'] =pd.to_datetime(historic.date)
    # makoing sure that no data before current year is brought in
    historic = historic[historic['date'] >= dt.datetime(today.year, 1, 1)]
    historic = historic.sort_values(by=['date'])
    # bring in the forecast for weatherr, whihc contains about 16 days worth of data (this dat get refreshed about once week)
    weather_pred = pd.read_csv('https://storage.googleapis.com/project-1050-data/weather_pred.csv')
    weather_pred['date_time'] = pd.to_datetime(weather_pred['Date time'])
    weather_pred = weather_pred[weather_pred['date_time'] >= now]
    weather_pred = weather_pred.sort_values(by=['date_time'])

    return live , historic , weather_pred