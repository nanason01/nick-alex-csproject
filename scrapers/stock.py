from typing import List
import alpaca_trade_api as tradeapi
from datetime import date, datetime, timedelta
import pandas as pd
from tqdm import tqdm
import time

import alpaca_trade_api as tradeapi

import reddit_app.sql.model as model

LOWEST_REDDIT_TIMESTAMP = '9/25/16'
HIGHEST_REDDIT_TIMESTAMP = '9/25/21'

def break_period_in_dates_list(start_date, end_date, days_per_step):
    '''Break period between start_date and end_date in steps of days_per_step days.'''
    step_start_date = start_date
    delta = timedelta(days=days_per_step)
    dates_list = []
    while end_date > (step_start_date + delta):
        dates_list.append((step_start_date, step_start_date+delta))
        step_start_date += delta
    dates_list.append((step_start_date, end_date))
    return dates_list


def format_timestep_list(timestep_list):
    '''Format dates in ISO format plus timezone. Note that first day starts at 00:00 and last day ends at 23:00hs.'''
    for i, d in enumerate(timestep_list):
        timestep_list[i] = (d[0].isoformat() + '-04:00', (d[1].isoformat().split('T')[0] + 'T23:00:00-04:00'))
    return timestep_list


def get_df_from_barset(barset):
    '''Create a Pandas Dataframe from a barset.'''
    df_rows = []
    for symbol, bar in barset.items():
        rows = bar.__dict__.get('_raw')
        for i, row in enumerate(rows):
            row['symbol'] = symbol
        df_rows.extend(rows)

    return pd.DataFrame(df_rows)

#TODO: add stepsize
# 2021-06-21T23:00:00-04:00
def download_data(symbols, start_date, end_date):
    '''Download data from REST manager for list of symbols, from start_date at 00:00hs to end_date at 23:00hs,
    and save it to filename as a csv file.'''
    aps = tradeapi.REST(key_id = 'AKVUIT2XXKCQ1W2W6TF6', 
                    secret_key = 'chgVtbcftCmvDQiCPzuqIl686obrsSzZ1hDCeENG', 
                    base_url = 'https://paper-api.alpaca.markets')

    timesteps = format_timestep_list(break_period_in_dates_list(start_date, end_date, 10))
    df = pd.DataFrame()
    for timestep in tqdm(timesteps):
        barset = aps.get_barset(symbols, 'day', limit=1000, start=timestep[0], end=timestep[1])
        df = df.append(get_df_from_barset(barset))
        time.sleep(0.1) 
    fileName = str(symbols) + '.csv'
    print(symbols, ": Writing Stock Data to File: ")
    df.to_csv(fileName)
    return df


def get_stock_data(symbol: str, startDate=LOWEST_REDDIT_TIMESTAMP, endDate=HIGHEST_REDDIT_TIMESTAMP) -> pd.DataFrame:
    '''Return df of daily changes in symbol'''
    df = download_data(
              symbols    = [symbol.upper()],
              start_date = datetime.strptime(LOWEST_REDDIT_TIMESTAMP, '%m/%d/%y'), 
              end_date   = datetime.strptime(HIGHEST_REDDIT_TIMESTAMP, '%m/%d/%y'))

    df = df.rename(columns={
        't': 'timestamp',
        'o': 'open',
        'h': 'high',
        'l': 'low',
        'c': 'close',
        'v': 'volume',
        'symbol': 'symbol',
    })

    db_conn = model.get_db()
    for i, row in df.iterrows():
        db_conn.execute(
            "INSERT OR IGNORE INTO stocks (symbol, utc, open_price, close_price, high, low, volume) "
            "VALUES ( ?, ?, ?, ?, ?, ?, ?)",
            (row['symbol'], row['timestamp'], row['open'], row['close'], row['high'], row['low'], row['volume'])
        )
        
    db_conn.commit()
    db_conn.close()
    
    print('Successfully grabbed data for', symbol)

# Call method.
aps = tradeapi.REST(key_id = 'AKVUIT2XXKCQ1W2W6TF6', 
                    secret_key = 'chgVtbcftCmvDQiCPzuqIl686obrsSzZ1hDCeENG', 
                    base_url = 'https://paper-api.alpaca.markets')

#print('input a symbol to grab data for:')
#symbol = input()
#symbol = 'GME'
#df = download_data(
#              symbols    = [symbol.upper()],
#              start_date = datetime.strptime(LOWEST_REDDIT_TIMESTAMP, '%m/%d/%y'), 
#             end_date   = datetime.strptime(HIGHEST_REDDIT_TIMESTAMP, '%m/%d/%y'))#


#df["t"] = pd.to_datetime(df["t"],)
#print(datetime.utcfromtimestamp(1632110400).strftime('%Y-%m-%dT%H:%M:%SZ'))

#print(df)


