from datetime import datetime, timedelta
import pandas as pd

import reddit_app.sql.model as model

from scrapers.stock import download_stock_data

def get_stock_data(symbol: str) -> pd.DataFrame:
    '''Return df of daily changes in symbol'''
    db_conn = model.get_db()
    df = pd.DataFrame(db_conn.execute(f'SELECT * FROM stocks WHERE symbol = "{symbol.upper()}"').fetchall())

    if df.empty:
        print(symbol, 'not present in database, downloading...')
        download_stock_data(symbol)
        df = pd.DataFrame(db_conn.execute(f'SELECT * FROM stocks WHERE symbol = "{symbol.upper()}"').fetchall())


    df = df.rename(columns={
        'close_price': 'close',
        'open_price': 'open', 
        'utc': 'timestamp',
    })

    print('im here')
    print(df)

    df.loc[:, 'timestamp'] = pd.to_datetime(df.loc[:, 'timestamp'])
    df = df.set_index('timestamp')
    return df.sort_index(inplace=True)

# takes stock data from db and makes it into timeseries.
def stockChartToTimeSeries(chart: pd.DataFrame):
    for x in range(0, len(chart['t'])):
        chart.loc[x, 't'] = str(datetime.fromtimestamp(chart.loc[x, 't']))
    chart.loc[:, 't'] = pd.to_datetime(chart.loc[:, 't'])
    chart = chart.set_index('t')
    chart.sort_index(inplace=True)
    return chart