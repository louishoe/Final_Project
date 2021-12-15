
def import_data():
    
    import pandas as pd
    import numpy as np
    #from datetime import date, timedelta, datetime
    import datetime as dt

    today = datetime.today()

    # Bring in the live data
    live = pd.read_csv('https://storage.googleapis.com/project-1050-data/live.csv')
    st_codes = pd.read_csv('https://storage.googleapis.com/project-1050-data/state_codes.csv')

    live = live.join(st_codes.set_index('State'), on="state")
    live.rename(columns={"temp":"Temperature", "Alpha code":"STATE"}, inplace=True)

    live['graph_date'] = live['UTC_date'] + ' '  + live['UTC_time']
    live['UTC_date'] = pd.to_datetime(live['UTC_date']).dt.date()
    dtm = today - dt.timedelta(1)
    dtm = datetime.strptime(str(dtm), '%Y-%m-%d').date()
    live = live[(live['UTC_date']>= dtm)]

    historic = pd.read_csv('https://storage.cloud.google.com/project-1050-data/historic-air.csv?authuser=3')
    historic['date'] =pd.to_datetime(historic.date)
    
    historic = historic[historic['date'] >= datetime(today.year, 1, 1)]
    historic = historic.sort_values(by=['date'])

    weather_pred = pd.read_csv('https://storage.cloud.google.com/project-1050-data/weather_pred.csv?authuser=3')
    weather_pred['date_time'] = pd.to_datetime(weather_pred['Date time'])
    weather_pred = weather_pred[weather_pred['date_time'] >= today]
    weather_pred = weather_pred.sort_values(by=['date_time'])

    return live , historic , weather_pred