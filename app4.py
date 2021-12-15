import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import requests
import sympy
import plotly.express as px
import plotly.graph_objs as go
import datetime 
from datetime import date, timedelta
from datetime import datetime as dt


live = pd.read_csv('https://storage.googleapis.com/project-1050-data/live.csv')
print(len(live))

# update the dataframe
live['graph_date'] = live['UTC_date'] + ' '  + live['UTC_time']
live['UTC_date'] = pd.to_datetime(live['UTC_date']).dt.date
today_dt = date.today()
today_dt = datetime.datetime.strptime(str(today_dt), '%Y-%m-%d').date()
live_df = live[(live['UTC_date'] == today_dt)]

daily_metrics = live_df.copy()
daily_metrics['hour'] = daily_metrics['UTC_time'].str[:2]
daily_metrics['hour'] = daily_metrics['hour'].astype(str).astype(int)
daily_metrics = daily_metrics.loc[daily_metrics.groupby(['city', 'state'])['hour'].idxmax()]
daily_metrics = daily_metrics[['city', 'state','temp', 'feels_like','weather_description']]
print(daily_metrics.head())


