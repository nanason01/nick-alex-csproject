from os import O_TRUNC
import pandas as pd
from datetime import datetime

import reddit_app.sql.model as model
from reddit_app.liwc.liwc import score_string


def get_df(sql_statement: str):
    db_conn = model.get_db()
    df = pd.DataFrame(db_conn.execute(sql_statement).fetchall())
    db_conn.close()
    return df


def find_where(words_in, subreddit: str = 'wallstreetbets', include_title: bool=True, include_selftext: bool=True):
    words_in = [word.lower() for word in words_in]

    find_str = f"SELECT * FROM posts WHERE subreddit = '{subreddit}' AND ("
    
    if include_title:
        for word in words_in:
            find_str += f"lower(title) LIKE '%{word}%' OR "

    if include_selftext:
        for word in words_in:
            find_str += f"lower(selftext) LIKE '%{word}%' OR "

    if not include_title and not include_selftext:
        print('warning: not including any fields to search for')
        return pd.DataFrame

    if words_in == []:
        print('warning: no words to search for')
        return pd.DataFrame
    
    find_str = find_str[:-4]
    find_str += ')'
    out_df = get_df(find_str)

    out_df['timestamp'] = pd.to_datetime(out_df['created_utc'])
    out_df = out_df.sort_values(by=['timestamp'])

    print('reddit df:', out_df)
    print('reddit cols:', out_df.columns)
    
    return out_df


def bucket_by_day(df) -> pd.DataFrame:
    df.timestamp = df.timestamp.apply(lambda d: d.strftime('%m/%d/%y'))
    return df['timestamp'].value_counts().rename_axis('timestamp').reset_index(name='num_posts')

def add_ratio(df_in, emotion: str):
    df_in[emotion] = df_in.apply(lambda row: score_string(row['selftext']), axis=1)

    return df_in