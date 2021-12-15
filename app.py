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
        html.P("Weather and Pollution Analysis in the United States by State:"),
        dcc.Dropdown(
        id='states', 
        options=[{'value': x, 'label': x} 
                 for x in live['state']],
        value="Rhode Island"),
        dcc.Graph(id='gen_metrics_temp', style={'display': 'inline-block'} ),
        dcc.Graph(id='gen_metrics_feels', style={'display': 'inline-block'} ),

        dcc.Graph(id="USA_MAP",style={'display': 'inline-block'}),
        dcc.Graph(id="bar_line", style={'display': 'inline-block'}),
        dcc.Graph(id="Weahter_forecast", style={'display': 'inline-block'})
        #dcc.Graph(id="AQI_Hist_line")
      
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
                        name='Temperature (°F)',
                        mode='lines+markers',
                        yaxis='y2')

    data = [line_graph, bar_graph]

    layout = go.Layout(title={'text': '{state}\'s Hourly Temperature and Pollution'.format(state=states),
         'y':0.9, # new
         'x':0.5,
         'xanchor': 'center',
         'yanchor': 'top' # new
        },
                       yaxis=dict(title='pm2.5',
                                   side='right'),
                       yaxis2=dict(title='Temperature (°F)',
                                   overlaying='y',
                                   side='left'))

    return go.Figure(data=data, layout=layout)


temp = '''@app.callback(
    Output("AQI_Hist_line", "figure"), 
    [Input("states", "value")])
def historic_air(states):
    """
    Returns the historic air quality by state capital for the last year
    """
    df = aqi_hist[aqi_hist['state'].eq(states)]
    fig = px.line(
                x = df['date'], 
                y = df[' pm25'],
                labels={'date':'Date', 
                ' pm25':'pm 2.5'}, 
            )
    fig.add_scatter(x=df['date'], y=df[' o3'], mode='lines', name = 'o3')
    fig.add_scatter(x=df['date'], y=df[' pm10'], mode='lines', name = 'pm 10')
    fig.add_scatter(x=df['date'], y=df[' no2'], mode='lines', name = 'no 2')
    fig.add_scatter(x=df['date'], y=df[' so2'], mode='lines', name = 'so 2')
    fig.add_scatter(x=df['date'], y=df[' co'], mode='lines', name = 'co')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='pm 2.5')
                              
    return fig
'''

@app.callback(
    Output("Weahter_forecast", "figure"), 
    [Input("states", "value")])
def weather_pre(states):
    df = weather_pred[weather_pred['state'].eq(states)]
    fig = px.line(
        x = df['date_time'],
        y = df['Temperature'],
        #error_y = df['Maximum Temperature']
        #error_y_minus= df['Minimum Temperature']
    )
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Temperture (°F)')
    fig.update_layout(title={'text':'{state}\'s Temperature Forecast'.format(state=states),
    'xanchor':'center',
    'yanchor':'top',
    'x':0.5})
    return fig

@app.callback(
    Output("gen_metrics_temp", 'figure'), 
    [Input("states", "value")])
def general_metrics(states):
    #daily_metrics = live.copy()
    daily_metrics = live[live['state']==states]
    daily_metrics['hour'] = daily_metrics['UTC_time'].str[:2]
    daily_metrics['hour'] = daily_metrics['hour'].astype(str).astype(int)
    daily_metrics = daily_metrics.loc[daily_metrics.groupby(['city', 'state'])['hour'].idxmax()]
    daily_metrics = daily_metrics[['city', 'state','Temperature', 'feels_like','weather_description']]
    
    fig = go.Figure(go.Indicator(
    mode = "number",
    value = daily_metrics.Temperature.values[0],
    number = {'suffix': " °F"},
    domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout(paper_bgcolor = "lightgray")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)