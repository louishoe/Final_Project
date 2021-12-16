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


# update to pull directly from local 'data' folder and move this script to the data folder 
## and have this script call that script
live = pd.read_csv('https://storage.googleapis.com/project-1050-data/live.csv')
print(len(live))

# update the dataframe
live['graph_date'] = live['UTC_date'] + ' '  + live['UTC_time']
live['UTC_date'] = pd.to_datetime(live['UTC_date']).dt.date
dt = date.today() - timedelta(1)
dt = datetime.datetime.strptime(str(dt), '%Y-%m-%d').date()
live_df = live[(live['UTC_date']>= dt)]

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
        # Blah blah blah
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

app = dash.Dash(__name__)

app.layout = html.Div([
        html.P("Current Weather in the United States:"),
        description(),
        dcc.Dropdown(
        id='states', 
        options=[{'value': x, 'label': x} 
                 for x in live_df['state']],
        value="Rhode Island"),
    dcc.Graph(id="line")
])

@app.callback(
    Output("line", "figure"), 
    [Input("states", "value")])
def display_graph(states):
    df = live_df[live_df['state'].eq(states)]


    bar_graph = go.Bar(x=df['graph_date'],
                    y=df['pm2.5'],
                    name='pm2.5',
                    yaxis='y1'
                    )
    line_graph = go.Line(x=df['graph_date'],
                        y=df['temp'],
                        name='Temperature',
                        mode='lines+markers',
                        yaxis='y2')

    data = [line_graph, bar_graph]

    layout = go.Layout(title='Temperature and Pollution',
                       yaxis=dict(title='pm2.5',
                                   side='right'),
                       yaxis2=dict(title='Temperature',
                                   overlaying='y',
                                   side='left'))

    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)