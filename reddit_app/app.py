from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from reddit_app.sql.reddit_filter import find_where, bucket_by_day
# from statsmodels.tsa.seasonal import seasonal_decompose

from reddit_app.stocks.stock_data import get_stock_data

"""
Columns of reddit db currently:

Unnamed: 0
postid
created_utc
score
upvote_ratio
total_awards_received
author
subreddit
title
selftext 
"""

# TODO: Update this to specify formatting, it will run much faster.

LOWEST_REDDIT_TIMESTAMP = '9/25/16'
HIGHEST_REDDIT_TIMESTAMP = '9/25/21'


app = dash.Dash(__name__)

merged_charts_tab = html.Div(
  children=[
    html.H1(id='H1', children='Time Series Decomposition Visualizer', style={'textAlign': 'center',
                                                                            'marginTop': 40, 'marginBottom': 40}),
    html.Div(id='merged-graph-placeholder'),
    dcc.Input(
      id="stock_in",
      placeholder='Enter a stongk...',
      type='text',
      value='GME',
      debounce=True),
    dcc.Input(
      id='reddit_terms',
      type='text',
      placeholder='search terms',
      value='gme gamestop',
      debounce=True),
    dcc.Checklist(
      id='flavor',
      options=[
        {'label': 'Price Observed', 'value': 'pObserved'},
        {'label': 'Price Trend', 'value': 'pTrend'},
        {'label': 'Price Seasonal', 'value': 'pSeasonal'},
        {'label': 'Price Residual', 'value': 'pResidual'},
        {'label': 'Mentions Observed', 'value': 'mObserved'},
        {'label': 'Mentions Trend', 'value': 'mTrend'},
        {'label': 'Mentions Seasonal', 'value': 'mSeasonal'},
        {'label': 'Mentions Residual', 'value': 'mResidual'},
      ],value=['pObserved','mObserved']
    )
  ]
)

'''           
unmerged_chart_depricated_tab = dcc.Tab(label = 'segundo', children= [
  dcc.Dropdown(
    id='mentions_graph_type',
      options=[
        {'label': 'Observed', 'value': 'observed'},
        {'label': 'Trend', 'value': 'trend'},
        {'label': 'Seasonal', 'value': 'seasonal'},
        {'label': 'Residual', 'value': 'resid'}
      ],
      value='observed'
    ), dcc.Dropdown(
      id='price_graph_type',
      options=[
        {'label': 'Observed', 'value': 'observed'},
        {'label': 'Trend', 'value': 'trend'},
        {'label': 'Seasonal', 'value': 'seasonal'},
        {'label': 'Residual', 'value': 'resid'}
      ],
      value='observed'
    ),
    html.H1("Individual: ", style={
            "margintop": 100, 'marginBottom': 40}),
    dcc.Dropdown(
      id='graph_type',
      options=[
        {'label': 'Observed', 'value': 'observed'},
        {'label': 'Trend', 'value': 'trend'},
        {'label': 'Seasonal', 'value': 'seasonal'},
        {'label': 'Residual', 'value': 'resid'}
      ],
      value='observed'
    ),
    html.Br(),
    html.Div(id='type_output'),
    dcc.Graph(id='stock_graph'),
    html.Div(id='reddit', children=[
      dcc.Input(
        id="stock_in_2",
        placeholder='Enter a stock to search reddit',
        type='text',
        value='GME',
        debounce=True),
      dcc.Input(
        id='reddit-search-in',
        type='text',
        placeholder='search terms',
        value='gme gamestop',
        debounce=True),
      dcc.Graph(id='stock_graph_2')
    ])
  ]
)
'''

app.layout = html.Div(id='parent', children=[
    merged_charts_tab,
  ]
)


@app.callback(
  Output(component_id='merged-graph-placeholder', component_property='children'),
  Input(component_id='flavor', component_property='value'),
  Input(component_id='stock_in', component_property='value'),
  Input('reddit_terms', 'value')
)
def decomposeGraph(graph_selection, symbol, terms):
    mentions_df = bucket_by_day(find_where(terms.split()))

    stock_df = get_stock_data(symbol)
    
    ''' TODO temp because I can't install seasonal_decompose
    graphed_dfs = []
    price_dfs = seasonal_decompose(stock_df, model='additive', period=30)
    mentions_dfs = seasonal_decompose(mentions_df, model='additive',period=30)
    
    # Price Switches
    if 'pObserved' in graph_selection:
      graphed_dfs.append(price_dfs.observed)
    if 'pTrend' in graph_selection:
      graphed_dfs.append(price_dfs.trend)
    if 'pSeasonal' in graph_selection:
      graphed_dfs.append(price_dfs.seasonal)
    if 'pResidual' in graph_selection:
      graphed_dfs.append(price_dfs.residual)
    # Mentions Switches
    if 'mObserved' in graph_selection:
      graphed_dfs.append(mentions_dfs.observed)
    if 'mTrend' in graph_selection:
      graphed_dfs.append(mentions_dfs.trend)
    if 'mSeasonal' in graph_selection:
      graphed_dfs.append(mentions_dfs.seasonal)
    if 'mResidual' in graph_selection:
      graphed_dfs.append(mentions_dfs.residual)
    
    out_df = graphed_dfs[0]
    for df in graphed_dfs[1:]:
      out_df = pd.merge_ordered(out_df, df)
    '''
    df = pd.merge_ordered(stock_df, mentions_df, on='timestamp')

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

    return dcc.Graph(figure=fig)

