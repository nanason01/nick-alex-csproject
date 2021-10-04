import pandas as pd
import plotly.express as px
from datetime import date, datetime

import sql.model as model

db_conn = model.get_db()

lookFor = ['gme', 'gamestop']

index = pd.date_range(start = "2018-07-01", end = "2022-12-12", freq = "D")
index = [pd.to_datetime(date, format='%Y-%m-%d').date() for date in index]

db_conn.close()

def get_df(sql_statement: str):
    db_conn = model.get_db()
    df = pd.DataFrame(db_conn.execute(sql_statement).fetchall())
    db_conn.close()
    return df


def find_where():
    df_with_gme = get_df("SELECT * FROM posts WHERE "
                         "subreddit = 'wallstreetbets' AND "
                         "(title LIKE '%gme%' OR title LIKE '%gamestop%' OR "
                         "selftext LIKE '%gme%' OR selftext LIKE '%gamestop%')")

    df_with_gme.created_utc = df_with_gme.created_utc.apply(lambda d: datetime.utcfromtimestamp(d).strftime('%Y-%m-%d'))

    return px.histogram(df_with_gme, x='created_utc')

    print(df_with_gme.shape)

def find_where(words_in, subreddit: str = 'wallstreetbets'):
    words_in = [word.lower() for word in words_in]

    find_str = f"SELECT * FROM posts WHERE subreddit = {subreddit} AND ("
    for word in words_in:
        find_str += f"lower(title) LIKE '%{word}%' OR lower(selftext) LIKE '%{word}%' OR "
    find_str = find_str[:-4]
    print(find_str)
    find_str += ')'

    out_df = get_df(find_str)
    out_df.created_utc = out_df.created_utc.apply(lambda d: datetime.utcfromtimestamp(d).strftime('%Y-%m-%d'))

    return out_df

find_where(['gme', 'gamestop'])