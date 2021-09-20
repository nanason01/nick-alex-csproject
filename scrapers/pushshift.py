from datetime import datetime, timedelta
import requests
import sys

PUSHSHIFT_URL = 'https://api.pushshift.io'
PUSHSHIFT_SUBREDDIT_URL = 'https://api.pushshift.io/reddit/search/submission/'
PUSHSHIFT_COMMENT_URL = 'https://api.pushshift.io/reddit/search/comment/'

HEADERS = {
    'User-Agent': 'nanason@his-Macbook'
}

def pushshift_subreddit_get(**kwargs):
    resp = requests.get(PUSHSHIFT_SUBREDDIT_URL, headers=HEADERS, params=kwargs)
    return resp.json()

def pushshift_comment_get(**kwargs):
    resp = requests.get(PUSHSHIFT_COMMENT_URL, headers=HEADERS, params=kwargs)
    return resp.json()

#resp_json = pushshift_subreddit_get()
#print(resp_json)


resp = requests.get('https://www.cnn.com/')
print(resp.json())