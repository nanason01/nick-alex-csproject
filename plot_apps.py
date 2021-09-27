import pandas as pd
import plotly.express as px
from datetime import datetime

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

find_where()
