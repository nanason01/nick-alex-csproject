import reddit_app.stocks.stock_data as stock_data
import reddit_app.sql.reddit_filter as reddit_filter

from dash import html, dcc
import dash
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)


def get_reddit_ts():
    df = reddit_filter.find_where(['gme', 'gamestop'])

def get_main_fig():
    df = stock_data.get_stock_data('GME', '11/16/20','11/20/20')

    print(df)

    fig = px.line(df, x= "timestamp", y = "high")

    return fig


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=get_main_fig()
    ),
])