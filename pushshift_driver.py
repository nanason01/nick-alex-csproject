from datetime import datetime
import sys

import formats.pushshift_post as pushshift_post
import scrapers.pushshift as pushshift
from config import PUSHSHIFT_LAST_TIMESTAMP_FILE

poster = pushshift_post.Pushshift_Post()

print('WARNING: USE CTRL+C TO END PROGRAM, NOT CTRL+Z OR PROGRESS IS A LOT HARDER TO RECOVER', file=sys.stderr)

try:
    with open(PUSHSHIFT_LAST_TIMESTAMP_FILE, 'r') as fin:
        last_lowest = int(fin.readline())
        count = int(fin.readline())
except FileNotFoundError:
    resp_json = pushshift.pushshift_subreddit_get(limit=1000, subreddit='wallstreetbets')
    
    for json_in in resp_json['data']:
        poster.digest_json(json_in)

    last_lowest = min([entry['created_utc'] for entry in resp_json['data']])

    count = len(resp_json['data'])
    print('processed', count)

try:
    while True:
        resp_json = pushshift.pushshift_subreddit_get(before=last_lowest, limit=1000, subreddit='wallstreetbets')

        for json_in in resp_json['data']:
            poster.digest_json(json_in)

        last_lowest = min([entry['created_utc'] for entry in resp_json['data']])

        count += len(resp_json['data'])
        print('processed', count)
except KeyboardInterrupt:
    with open(PUSHSHIFT_LAST_TIMESTAMP_FILE, 'w') as fout:
        fout.write(str(last_lowest))
        fout.write('\n')
        fout.write(str(count))