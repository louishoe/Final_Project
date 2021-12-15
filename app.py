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

#live, aqi_hist, weather_pred = import_data()
live, aqi_hist, weather_pred = import_data()

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
        Place Description Here. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

app = dash.Dash(__name__)

app.layout = html.Div([
        html.P("Current Weather in the United States:"),
        dcc.Dropdown(
        id='states', 
        options=[{'value': x, 'label': x} 
                 for x in live['state']],
        value="Rhode Island"),
    dcc.Graph(id="USA_MAP",style={'display': 'inline-block'}),
    dcc.Graph(id="bar_line", style={'display': 'inline-block'})
    #display_choropleth(live)
])

@app.callback(
    Output("USA_MAP", "figure"), 
    Input("states", "value"),)
def display_choropleth(df):
    df = live
    fig = px.choropleth(df, color="Temperature", locations="STATE", locationmode="USA-states", scope="usa")
    fig.update_layout(title={'text':'Current Temperature by State',
    'xanchor':'center',
    'yanchor':'top',
    'x':0.5})

    return fig

@app.callback(
    Output("bar_line", "figure"), 
    [Input("states", "value")])
def display_graph(states):
    df = live[live['state'].eq(states)]


    bar_graph = go.Bar(x=df['graph_date'],
                    y=df['pm2.5'],
                    name='pm2.5',
                    yaxis='y1'
                    )
    line_graph = go.Line(x=df['graph_date'],
                        y=df['Temperature'],
                        name='Temperature',
                        mode='lines+markers',
                        yaxis='y2')

    data = [line_graph, bar_graph]

    layout = go.Layout(title={'text': 'Temperature and Pollution',
         'y':0.9, # new
         'x':0.5,
         'xanchor': 'center',
         'yanchor': 'top' # new
        },
                       yaxis=dict(title='pm2.5',
                                   side='right'),
                       yaxis2=dict(title='Temperature',
                                   overlaying='y',
                                   side='left'))

    return go.Figure(data=data, layout=layout)





if __name__ == '__main__':
    app.run_server(debug=True)