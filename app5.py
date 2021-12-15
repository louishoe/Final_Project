import dash
from dash import dash_table, Dash, html, Input, Output, callback_context
import dash_bio as dashbio
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
# pip install dash_bio
aqi_hist = pd.read_csv('https://storage.googleapis.com/project-1050-data/2021_AQI_hist.csv')
aqi_hist['month'] = pd.DatetimeIndex(aqi_hist['date']).month
aqi_hist['day'] = pd.DatetimeIndex(aqi_hist['date']).day
print(aqi_hist.head())
aqi_hist = aqi_hist[['state','city','month', 'day', ' pm25', ' o3', ' pm10', ' no2',' so2', ' co']]
aqi_hist_month = aqi_hist.groupby(['state', 'city','month', 'day'], as_index=False).mean()
aqi_hist_month = aqi_hist_month.fillna(0)
print(aqi_hist_month.head(5))



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

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='states', 
        options=[{'value': x, 'label': x} 
                 for x in aqi_hist['state']],
        value="Rhode Island"),
    html.Button(' pm25', id='btn-nclicks-1', n_clicks=0),
    html.Button(' o3', id='btn-nclicks-2', n_clicks=0),
    html.Button(' pm10', id='btn-nclicks-3', n_clicks=0),
    html.Button(' no2', id='btn-nclicks-4', n_clicks=0),
    html.Button(' so2', id='btn-nclicks-5', n_clicks=0),
    html.Button(' so', id='btn-nclicks-6', n_clicks=0),
    #html.Div(id='container-button-timestamp'),
    dcc.Graph(id="graph")
])

@app.callback(
    Output('graph', 'figure'),
    [Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    Input('btn-nclicks-6', 'n_clicks'),
    Input("states", "value")])

def displayClick(btn1, btn2, btn3, btn4, btn5, btn6, states):
    df = aqi_hist[aqi_hist['state'].eq(states)]
    mapping = {1:' pm25', 2:' o3', 3:' pm10', 4:' no2',5:' so2',6:' co'}
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    print(changed_id)
    if 'btn-nclicks-1' in changed_id:
        print('hi')
        # df = df[['month',mapping[btn1]]]
        # print(df.head())
        # fig = px.bar(df, x=mapping[btn1], y="month", orientation='h', barmode="group")
        # fig.update_layout(width=int(500))
        # fig.update_layout(height=int(800))
        # fig.update_xaxes(title_text=' ')
        # fig.update_yaxes(title_text='Today\'s Air Quality Index by Pollutant')
        # # fig = px.imshow(df)
        # # print("here")

        # return fig
        
    elif 'btn-nclicks-2' in changed_id:
        df = aqi_hist[aqi_hist['state'].eq(states)]
    elif 'btn-nclicks-3' in changed_id:
        df = aqi_hist[aqi_hist['state'].eq(states)]
    else:
        msg = 'None of the buttons have been clicked yet'
    #return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
# def display_graph(states):
#     df = aqi_hist[aqi_hist['state'].eq(states)]
    
#     dashbio.AlignmentChart(
#         id='my-default-alignment-viewer',
#         data=df,
#         height=900,
#         tilewidth=30,
#     ),

#     return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)