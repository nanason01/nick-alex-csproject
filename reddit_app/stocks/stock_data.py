from datetime import datetime, timedelta
import pandas as pd

import reddit_app.sql.model as model

def get_stock_data(symbol: str) -> pd.DataFrame:
    '''Return df of daily changes in symbol'''
    db_conn = model.get_db()
    df = pd.DataFrame(db_conn.execute(f'SELECT * FROM stocks WHERE symbol = "{symbol.upper()}"').fetchall())

    if df.empty:
        print('WARNING:', symbol, 'not present in database')
        print(f'try running: $ echo "{symbol}" | python3 scrapers/stock.py')

    df = df.rename(columns={
        'close_price': 'close',
        'open_price': 'open', 
        'utc': 'timestamp',
    })

    df.timestamp = df.timestamp.apply(lambda d: datetime.utcfromtimestamp(d).strftime('%m/%d/%y'))
    
    return df
