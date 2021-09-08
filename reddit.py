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

def print_comments(comment_jsons):
    for comment_json in comment_jsons:
        print(comment_json['data']['body'])

        if comment_json['data']['replies'] != '':
            print('Has children:')
            if comment_json['data']['replies']:
                print_comments(comment_json['data']['replies']['data']['children'])

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

print('these are the fields in a comment')
resp_json = reddit_get('https://oauth.reddit.com/r/python/comments/pihblq')
print(resp_json[0]['data']['children'][0]['data'].keys())

'''
Some notes on the json response structure:

everything is wrapped in a dict with 'kind' and 'data' fields,
where 'kind' indicates the type of the following data

anything that could be a list is then wrapped in the 'children' of 'data' of a listing-kind json

comments have a 'replies' field which is either empty string or a listing object
comments text is 'body'
posts title is 'title' and content is in 'selftext'

we can add a after and limit field to the header to specify the end time range and increase number of posts

get for posts: https://oauth.reddit.com/r/<subreddit>/hot
get for comments: https://oauth.reddit.com/r/<subreddit>/comments/<postid>
'''