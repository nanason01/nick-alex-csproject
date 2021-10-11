import reddit_app.stocks.stock_data as stock_data
from dash import html, dcc
import dash
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = stock_data.get_stock_data('GME', '12/11/20','05/01/21')
fig = px.line(df, x= "t", y = "h")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
])