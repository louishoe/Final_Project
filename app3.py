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
today_dt = date.today()
today_dt = datetime.datetime.strptime(str(today_dt), '%Y-%m-%d').date()
live_df = live[(live['UTC_date'] == today_dt)]

print(live_df.columns)
pol_stats = live_df[['state','pm2.5','co','no2','o3']]
pol_stats = pol_stats.groupby('state', as_index=False).mean()
pol_stats = pol_stats.fillna(0)

usa_stats = pol_stats[['pm2.5','co','no2','o3']]
usa_stats['country'] = 'USA'
cols = ['country','pm2.5','co','no2','o3']
usa_stats = usa_stats[cols]
usa_stats = usa_stats.groupby('country', as_index=False).mean()
print(type(usa_stats))
print(usa_stats.head())
# usa_stats = usa_stats.groupby('USA', as_index=False).mean()




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
    dcc.Graph(id="bar")
])

@app.callback(
    Output("bar", "figure"), 
    [Input("states", "value")])
def display_graph(states):
    df = pol_stats[pol_stats['state'].eq(states)]
    df = df.melt(id_vars=["state"], 
        var_name="Pollution", 
        value_name="Value")
    df_usa = usa_stats.melt(id_vars=["country"], 
        var_name="Pollution", 
        value_name="Value")

    concat_df = pd.concat([df, df_usa.rename(columns={'country':'state'})])


    fig = px.bar(concat_df, x="Value", y="Pollution", orientation='h', color='state', barmode="group")
    fig.update_layout(width=int(500))
    fig.update_layout(height=int(800))
    fig.update_xaxes(title_text=' ')
    fig.update_yaxes(title_text='Today\'s Air Quality Index by Pollutant')
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)