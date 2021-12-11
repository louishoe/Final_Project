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

#start the app
app = dash.Dash(__name__)

#import data:
gs = 'gs://live.csv/'
df = pd.read_csv(gs+'data_file.csv')

#set up your components and html needed
app.layout = html.Div([
    html.H1("Weather Map (Test)", style={'text-align': 'center'}),
    
    dcc.Dropdown(id="Select_Year",
                options=[
                    {"label": "2016", "value": 2016},
                    {"label": "2016", "value": 2017},
                    {"label": "2016", "value": 2018},
                    {"label": "2016", "value": 2019},
                    {"label": "2016", "value": 2020},
                    {"label": "2016", "value": 2021}
                ])
])