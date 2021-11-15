import reddit_app.stocks.stock_data as stock_data
import reddit_app.sql.reddit_filter as reddit_filter
from liwc.liwc_cols_with_nums import LIWC_NUM_TO_EMOTION

from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

app = dash.Dash(__name__)


def get_reddit_ts(filter_words):
    df = reddit_filter.find_where(filter_words)

    df = df.rename(columns={'created_utc': 'timestamp'})

    df = df['timestamp'].value_counts().rename_axis('timestamp').reset_index(name='num_posts')

    print(filter_words)
    print(df)

    return df

def get_stock_ts(symbol: str):
    return stock_data.get_stock_data(symbol)

def get_main_fig(symbol: str, reddit_terms):
    reddit_df = get_reddit_ts(reddit_terms)
    
    stock_df = get_stock_ts(symbol.upper())

    df = stock_df.merge(reddit_df, how='outer', on='timestamp')
    df['num_posts'] = df['num_posts'].fillna(0)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['close'], name="closing price"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['num_posts'], name="daily reddit mentions"),
        secondary_y=True,
    )

    fig.update_layout(title_text="Time series of reddit mentions and stock performance")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Closing Price", secondary_y=False)
    fig.update_yaxes(title_text="Reddit Posts Mentioning", secondary_y=True)

    return fig


app.layout = html.Div(children=[
    html.H1(children='Time Series Comparison Web App'),

    dcc.Input(id='symbol-in', type='text', placeholder='symbol', value='gme'),
    dcc.Input(id='reddit-search-in', type='text', placeholder='search terms', value='gme gamestop'),

    html.Div(id='emotion-out'),
    dcc.Dropdown(
        id='emotion-in',
        options=[{'label': emotion, 'value': emotion} for emotion in LIWC_NUM_TO_EMOTION.values()],
        multi=True
    ),

    html.Div(id='graph-placeholder')
])

# TODO:
# add figure that overlays multiple ratios of that
# add callback to pipe those together

@app.callback(
    Output('emotion-out', 'children'),
    Input('emotion-in', 'value')
)
def temp_output_emotions(selection):
    print(selection)
    return selection

@app.callback(
    Output('graph-placeholder', 'children'),
    Input('symbol-in', 'value'),
    Input('reddit-search-in', 'value')
)
def render_fig(symbol, reddit_terms):
    if symbol is None or symbol.upper() not in ['GME', 'TSLA', 'AMC']:
        return dcc.Graph()

    print(reddit_terms)
    if reddit_terms is None:
        reddit_terms = ''

    return dcc.Graph(figure=get_main_fig(symbol, reddit_terms.split()))