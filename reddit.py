import json
from datetime import datetime, timedelta
import requests
import sys

headers = {
        'user-agent': 'nick-alex-csproject/nicks-macbook'
}
header_expires_at = datetime.now()

def update_header_auth():
    global header_expires_at
    if datetime.now() < header_expires_at:
        return

    auth = requests.auth.HTTPBasicAuth('WRGvCG1hOlxn3KLPVbLtOA', 'p0N29IbptceAI-h2VNdpGpf-P0xhVQ')

    login_data = {'grant_type': 'password',
            'username': 'nanason01',
            'password': '_,a4YNcwT??<4gS'}

    auth_res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=login_data, headers=headers)

    if 'error' in auth_res.json():
        print('Error fetching auth token:', auth_res.json()['error'], file=sys.stderr)
        exit()

    else:
        header_expires_at = datetime.now() + timedelta(seconds=auth_res.json()['expires_in'])
        token = auth_res.json()['access_token']
        headers['Authorization'] = f'bearer {token}'

def reddit_get(url: str):
    update_header_auth()

    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print('Error sending request:', resp.reason)
        exit()

resp_json = reddit_get("https://oauth.reddit.com/r/python/hot")

interesting_things = [
    'title',
    'ups',
    'downs',
    'score',
    'upvote_ratio',
    'view_count',
    'num_comments',
    'media',
    'num_reports',
    'selftext',
]

for thing in interesting_things:
    print(f'{thing}:', resp_json['data']['children'][0]['data'][thing])

print(resp_json['data']['children'][0]['data'])


resp_json = reddit_get('https://oauth.reddit.com/r/python/comments/pihblq')
print('\n\n', resp_json[0]['data']['children'][0])