import reddit_app.stocks.stock_data as stock_data
import reddit_app.sql.reddit_filter as reddit_filter

from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

LOWEST_REDDIT_TIMESTAMP = '9/25/16'
HIGHEST_REDDIT_TIMESTAMP = '9/25/21'

def get_reddit_ts():
    df = reddit_filter.find_where(['gme', 'gamestop'])

def get_stock_ts(symbol: str):
    return stock_data.get_stock_data(symbol, LOWEST_REDDIT_TIMESTAMP, HIGHEST_REDDIT_TIMESTAMP)

def get_main_fig(symbol: str):
    df = get_stock_ts(symbol.upper())

    print(df)

    fig = px.line(df, x= "timestamp", y = "close")

    return fig


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    dcc.Input(id='symbol_in', type='text', placeholder='symbol'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='ts-graph',
        figure=None
    ),
])

@app.callback(
    Output('ts-graph', 'figure'),
    Input('symbol_in', 'value')
)
def render_fig(symbol):
    print('here')
    if symbol.upper() not in ['GME', 'TSLA', 'AMC']:
        return None
    return get_main_fig(symbol)