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
gs = 'gs://live.csv/'
df = pd.read_csv(gs+'data_file.csv')

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

def weather_figure():
    
    live = pd.read_csv('live.csv')  ##import data 
    x = live['date']
    y = live['temp']
    fig_line = px.line(live,
                        x = x, 
                        y = y, 
                        color = "city",
                        hover_data = ["city"], 
                        line_shape="spline",
                        render_mode="svg"
                        height = 700)
                            
    fig_line.update_layout(legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1))
                              
    fig_line.update_layout(font=dict(size = 20))
                              
    fig_line.update_layout(template='plotly_white')
    
    return html.Div(children=[dcc.Graph(figure = fig_line, 
                                        className = 'offset-by-one nine columns', 
                                        style={'paddingLeft': '5%'})], 
                    className="row")

def forecast_figure():
    
    forecast = pd.read_csv
    x = forecast['date']
    fig = px.parallel_coordinates(forecast,
                                color="species_id",
                                labels={"species_id": "Species",
                    "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                    "petal_width": "Petal Width", "petal_length": "Petal Length", },
                        color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2)

    fig_bar.update_layout(xaxis_type='category')
    
    fig_bar.update_layout(legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1)) 
    
    fig_bar.update_layout(font=dict(size = 20))
    
    fig_bar.update_layout(template='plotly_dark',
                          plot_bgcolor='#2d3339',
                          paper_bgcolor='#5b6571')
    
    fig_bar.update_xaxes(showgrid = False)
    fig_bar.update_yaxes(gridcolor='#717e8e', 
                         layer = 'above traces')
    
    return html.Div(children=[dcc.Graph(figure = fig_bar, 
                                        className = 'offset-by-one nine columns', 
                                        style={'paddingLeft': '5%'})], 
                    className="row")


app = dash.Dash(__name__)

app.layout = html.Div(
    className="main",
    children=[
        html.H2("Temperature predictions"),
        dcc.Input(id="lat", value='41.82831'),
        dcc.Input(id="long", value='-71.40100'),
        html.Button("Go", id="go"),
        dcc.Graph(id='graph')
    ]
)

@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='go', component_property='n_clicks'),
    State(component_id='lat', component_property='value'),
    State(component_id='long', component_property='value'),
)
def update_graph(n_clicks, lat, long):
    response = requests.get(f"gs://project-1050-data/data_file.csv")
    forecastUrl = response.json()["properties"]["forecastHourly"]
    response = requests.get(forecastUrl)
    hours = response.json()['properties']['periods']
    df = pd.DataFrame({
        'hours from now': range(len(hours)),
        'temperature (F)': [hour['temperature'] for hour in hours],
    })
    return px.line(df, x = 'hours from now', y = 'temperature (F)')

app.run_server(debug=True, host="0.0.0.0")