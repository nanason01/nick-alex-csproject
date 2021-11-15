from datetime import datetime
from sqlite3.dbapi2 import Timestamp

from numpy.lib.ufunclike import _deprecate_out_named_y
from pandas.core.indexes import period
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from scrapers.stock import download_data

# For mentions
from reddit_app.app import get_main_fig

# for use with decomposition
# TODO: add to requirements
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
""" 
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
#sf = pd.read_csv('teslaWallstreetbets.csv')
# Set object type of dates to datetime64[ns]
# TODO: Update this to specify formatting, it will run much faster.
#sf["created_utc"] = pd.to_datetime(sf["created_utc"])

#sf = sf.set_index('created_utc')
LOWEST_REDDIT_TIMESTAMP = '9/25/16'
HIGHEST_REDDIT_TIMESTAMP = '9/25/21'

# use .indexes to use indexes blah blah blah.
#fig = px.line(sf, x=sf.index, y='score')
def toTimeSeries2(chart):
  #for x in range(0,len(chart['t'])):
  #  chart['t'][x] = str(datetime.fromtimestamp(chart['t'][x]))  
  chart['timestamp'] = pd.to_datetime(chart['timestamp'])
  chart = chart.set_index('timestamp')
  chart.sort_index(inplace=True)
  return chart
# takes stock data from api and makes it into timeseries. 
def toTimeSeries(chart):
  for x in range(0,len(chart['t'])):
    #chart['t'][x] = str(datetime.fromtimestamp(chart['t'][x]))
    chart.loc[x,'t'] = str(datetime.fromtimestamp(chart.loc[x,'t']))    
  chart.loc[:,'t'] = pd.to_datetime(chart.loc[:,'t'])
  chart = chart.set_index('t')
  chart.sort_index(inplace=True)
  return chart
  
def decomposeTimeSeries(series, type_input):
  #print((series).tail)
  stock_chart = seasonal_decompose(series, model='additive', period=30)
  if type_input == 'Output: observed':
    #print("Returning Decomp, Original")
    return stock_chart.observed
  elif type_input == 'Output: trend':
    #print("Returning Decomp, trend")
    return stock_chart.trend
  elif type_input == 'Output: seasonal':  
    #print("Returning Decomp, Seasonal")
    return stock_chart.seasonal
  elif type_input == 'Output: resid':  
    return stock_chart.resid

app = dash.Dash(__name__)
# TODO: RESTRUCUTURE TO USE DIVS
app.layout = html.Div(id = 'parent', children = [
      html.H1(id = 'H1', children = 'Time Series Decomposition Visualizer', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
      dcc.Graph(id="merged_graph"),
      dcc.Input(
        id="stonk_in",
        placeholder='Enter a stongk...',
        type='text',
        value='GME', 
        debounce=True),
      dcc.Checklist(
        id='flavor',
        options=[
          {'label': 'Price', 'value': 'p'},
          {'label': 'Mentions', 'value': 'm'}
        ]
      ),
      dcc.Dropdown(
        id='graph_type',
        options =[
            {'label': 'Observed', 'value': 'observed'},
            {'label': 'Trend', 'value': 'trend'},
            {'label': 'Seasonal', 'value': 'seasonal'},
            {'label': 'Residual', 'value': 'resid'}
        ],
        value='observed'
      ),
      html.Br(),
      html.Div(id='type_output'),
      dcc.Graph(id='stonk_graph'),

      html.Div(id='reddit', children=[
        dcc.Input(
            id="stonk_in_2",
            placeholder='Enter a stongk serj reddit...',
            type='text',
            value='GME', 
            debounce=True),
        dcc.Input(
            id='reddit-search-in', 
            type='text', 
            placeholder='search terms',
            value='gme gamestop',
            debounce=True),
        dcc.Graph(id='stonk_graph_2')
      ])
    ])
    
@app.callback(
    Output(component_id='type_output', component_property='children'),
    Input(component_id='graph_type', component_property= 'value')
)
def update_output(input_value):
    print("Dropdown Change: ", input_value)
    return 'Output: {}'.format(input_value)

@app.callback(
  Output(component_id='stonk_graph', component_property= 'figure'),
  Input(component_id='stonk_in', component_property= 'value'),
  Input('type_output', component_property = 'children')
)
def updateGraph(input_value, type_input):
  print("Input Stock", input_value)
  print("Type Stock", type_input)
  symbol = input_value
  csvName = "['" + str(symbol).upper() + "'].csv"
  try:
    with open(csvName) as f:
      print("File present")
  except FileNotFoundError:
      print('File is not present')
      download_data(
        symbols    = [symbol.upper()],
        start_date = datetime.strptime(LOWEST_REDDIT_TIMESTAMP, '%m/%d/%y'), 
        end_date   = datetime.strptime(HIGHEST_REDDIT_TIMESTAMP, '%m/%d/%y')
      )
      csvName = "['" + str(symbol).upper() + "'].csv"

  stock_chart = pd.read_csv(csvName)
  stock_chart  = toTimeSeries(stock_chart.loc[:,['t','h']])
  stock_chart = decomposeTimeSeries(stock_chart, type_input)
  stock_chart = (pd.DataFrame(stock_chart))
  fig = px.line(stock_chart,template='plotly_dark')
                
  return fig

@app.callback(
  Output(component_id='stonk_graph_2', component_property= 'figure'),
  Input(component_id='stonk_in_2', component_property= 'value'),
  Input('reddit-search-in', 'value')
)
def updateMentionsGraph(symbol, reddit_terms):
  print("Mentions: Input Stock: ", symbol)
  print("Mentions: Reddit Terms: ", reddit_terms)
  if reddit_terms is None:
      reddit_terms = ''
  #return dcc.Graph(figure=get_main_fig(symbol, reddit_terms.split()))
  x = get_main_fig(symbol, reddit_terms.split())
  x = toTimeSeries2(x)
  x = pd.DataFrame(x)
  return px.line(x,template='plotly_dark')

@app.callback(
  Output(component_id='merged_graph', component_property= 'figure'),
  Input(component_id='flavor', component_property= 'value'),
  Input(component_id='stonk_in_2', component_property= 'value'),
  Input('reddit-search-in', 'value')
)
def craftGraph(comb, ticker, terms):
  # mentions df.
  x = toTimeSeries2(get_main_fig(ticker, terms.split()))
  # make other callbacks member functions now
  # temp copy and paste.
  symbol = ticker
  csvName = "['" + str(symbol).upper() + "'].csv"
  try:
    with open(csvName) as f:
      print("File present")
  except FileNotFoundError:
      print('File is not present')
      download_data(
        symbols    = [symbol.upper()],
        start_date = datetime.strptime(LOWEST_REDDIT_TIMESTAMP, '%m/%d/%y'), 
        end_date   = datetime.strptime(HIGHEST_REDDIT_TIMESTAMP, '%m/%d/%y')
      )
      csvName = "['" + str(symbol).upper() + "'].csv"

  stock_chart = pd.read_csv(csvName)
  #stock_chart  = toTimeSeries(stock_chart[['t','h']])
  stock_chart  = toTimeSeries(stock_chart.loc[:,['t','h']])
  trace0 = go.Scatter(
    x = x.index,
    y = x.iloc[:,0] / 100,
    mode = 'lines',
    name = 'Mentions'
  )
  trace1 = go.Scatter(
    x = stock_chart.index,
    y = stock_chart.iloc[:,0],
    mode = 'lines',
    name = 'Cost'
  )
  if 'p' in comb and 'm' in comb:
    data = [trace0, trace1]
  elif 'p' in comb:
    data = [trace1]
  elif 'm' in comb:
    data = [trace0]
  else: 
    data = 0
      
  
  fig = go.Figure(data = data)
  return fig


if __name__ == '__main__':
    app.run_server(debug=True)

