
def import_data():
    
    import pandas as pd
    import numpy as np
    #from datetime import date, timedelta, datetime
    import datetime as dt

    now = dt.datetime.utcnow()
    today = now.date()

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
    
    #today_dt = dt.datetime.strptime(str(now), '%Y-%m-%d').date()

    today_live = live[(live['UTC_date'] == today)]
    
    # Bring in historical AQI data:
    historic = pd.read_csv('https://storage.googleapis.com/project-1050-data/2021_AQI_hist.csv')
    historic['date'] =pd.to_datetime(historic.date)
    # makoing sure that no data before current year is brought in
    historic = historic[historic['date'] >= dt.datetime(today.year, 1, 1)]
    historic = historic.sort_values(by=['date'])

    historic['month'] = pd.DatetimeIndex(historic['date']).month
    historic['day'] = pd.DatetimeIndex(historic['date']).day
    # bring in the forecast for weatherr, whihc contains about 16 days worth of data (this dat get refreshed about once week)
    weather_pred = pd.read_csv('https://storage.googleapis.com/project-1050-data/weather_pred.csv')
    weather_pred['date_time'] = pd.to_datetime(weather_pred['Date time'])
    weather_pred = weather_pred[weather_pred['date_time'] >= now]
    weather_pred = weather_pred.sort_values(by=['date_time'])


    pol_stats = today_live.copy()
    pol_stats = pol_stats[['state','aqi']]
    pol_stats['aqi'] = pol_stats['aqi'].astype(float)
    #usa_stats = pol_stats[['aqi']]
    #usa_stats['country'] = 'USA'
    #cols = ['country','aqi']
    #usa_stats = usa_stats[cols]
    #usa_stats = usa_stats.groupby('country', as_index=False).mean()



    return live , historic , weather_pred, pol_stats 