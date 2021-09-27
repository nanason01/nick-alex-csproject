from datetime import datetime, timedelta
import requests
import time
import json

PUSHSHIFT_URL = 'https://api.pushshift.io'
PUSHSHIFT_SUBREDDIT_URL = 'https://api.pushshift.io/reddit/search/submission/'
PUSHSHIFT_COMMENT_URL = 'https://api.pushshift.io/reddit/search/comment/'

HEADERS = {
    'User-Agent': 'nanason@his-Macbook'
}

def pushshift_subreddit_get(**kwargs):
    while True:
        resp = requests.get(PUSHSHIFT_SUBREDDIT_URL, headers=HEADERS, params=kwargs)
        if resp.status_code == 429:
            print('waiting a sec')
            time.sleep(5)
            continue

        try:
            return resp.json()
        except json.JSONDecodeError:
            print('json decode error in getting')
            continue
        except:
            print('unexpected error in getting')
            continue

def pushshift_comment_get(**kwargs):
    resp = requests.get(PUSHSHIFT_COMMENT_URL, headers=HEADERS, params=kwargs)
    return resp.json()

#resp_json = pushshift_subreddit_get()
#print(resp_json)

'''
resp = pushshift_subreddit_get(subreddit='wallstreetbets')
utcs = [entry['created_utc'] for entry in resp['data']]
lowest, highest = min(utcs), max(utcs)
print('range:', lowest, 'to', highest)


resp = pushshift_subreddit_get(before=lowest, subreddit='wallstreetbets')
utcs = [entry['created_utc'] for entry in resp['data']]
lowest1, highest1 = min(utcs), max(utcs)
print('range:', lowest1, 'to', highest1)

resp = pushshift_subreddit_get(before=highest, subreddit='wallstreetbets')
utcs = [entry['created_utc'] for entry in resp['data']]
lowest2, highest2 = min(utcs), max(utcs)
print('range:', lowest2, 'to', highest2)
'''