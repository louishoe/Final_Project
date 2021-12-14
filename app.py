

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

# update to pull directly from local 'data' folder and move this script to the data folder 
## and have this script call that script
live = pd.read_csv('https://storage.googleapis.com/project-1050-data/live.csv')
st_codes = pd.read_csv('https://storage.googleapis.com/project-1050-data/state_codes.csv')
st_codes["STATE"] = st_codes["Alpha code"]

live = live.join(st_codes.set_index('State'), on="state")

def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('Blownhither', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/blownhither/'), #change this as it references personal git page
    ], className="row")

def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # Energy Planner
        As of today, 138 cities in the U.S. have formally announced 100% renewable energy goals or
        targets, while others are actively considering similar goals. Despite ambition and progress,
        conversion towards renewable energy remains challenging.
        Wind and solar power are becoming more cost effective, but they will always be unreliable
        and intermittent sources of energy. They follow weather patterns with potential for lots of
        variability. Solar power starts to die away right at sunset, when one of the two daily peaks
        arrives (see orange curve for load).
        **Energy Planner is a "What-If" tool to assist making power conversion plans.**
        It can be used to explore load satisfiability under different power contribution with 
        near-real-time energy production & consumption data.
        ### Data Source
        Energy Planner utilizes near-real-time energy production & consumption data from [BPA 
        Balancing Authority](https://www.bpa.gov/news/AboutUs/Pages/default.aspx).
        The [data source](https://transmission.bpa.gov/business/operations/Wind/baltwg.aspx) 
        **updates every 5 minutes**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

app = dash.Dash(__name__)

app.layout = html.Div([
        html.P("Current Weather in the United States:"),
        dcc.Dropdown(
        id='states', 
        options=[{'value': x, 'label': x} 
                 for x in live['state']],
        value="Rhode Island"),
    dcc.Graph(id="choropleth")
    #display_choropleth(live)
])

@app.callback(
    Output("choropleth", "figure"), 
    Input("states", "value"),)
def display_choropleth(df):
    df = live
    fig = px.choropleth(df, color="temp", locations="STATE", locationmode="USA-states", scope="usa")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title={'text':'Weather by State',
    'xanchor':'center',
    'yanchor':'top',
    'x':0.5})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)