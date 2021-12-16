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
from data_manipulation import import_data
from weather_visuals import icons
import calendar

live, aqi_hist, weather_pred, pol_stats, region_df = import_data()

daily_metrics = live[live['state']
daily_metrics['hour'] = daily_metrics['UTC_time'].str[:2]
daily_metrics['hour'] = daily_metrics['hour'].astype(str).astype(int)
daily_metrics = daily_metrics.loc[daily_metrics.groupby(['city', 'state'])['hour'].idxmax()]
daily_metrics = daily_metrics[['city', 'state','Temperature', 'feels_like','weather_description']]
    