from datetime import datetime
import pathlib
import sqlite3
import sys

from requests.api import post

from config import REDDIT_POST_FIELDS, REDDIT_POSTS_DIR, SUBREDDIT_TO_INT


def utc_to_dt(timestampValue):
   # get the UTC time from the timestamp integer value.
   d = datetime.utcfromtimestamp( int(timestampValue) )

   # calculate time difference from utcnow and the local system time reported by OS
   offset = datetime.now() - datetime.utcnow()

   # Add offset to UTC time and return it
   return d + offset

class Pushshift_Post:
    # store a json as a file with proper placement and format
    def digest_json(self, json_in, db_conn):
        
        db_conn.execute(
            "INSERT OR IGNORE INTO posts (postid, created_utc, score, upvote_ratio, total_awards_received, author, subreddit, title, selftext) "
            "VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (json_in['id'], json_in['created_utc'], json_in.get('score', 0), json_in.get('upvote_ratio', 0), json_in.get('total_awards_received', 0),
            json_in.get('author', '__no_author'), json_in['subreddit'], json_in.get('title', 'empty'), json_in.get('selftext', 'empty'))
        )

    # return a dict of important fields from a previously stored file
    # equivalent to the stripped 'data' field of the json_in
    def digest_file(self, filename):
        assert False
        if not pathlib.Path(filename).exists():
            print('Error:', filename, 'does not exist', file=sys.stderr)
            return
        
        with open(filename, 'r') as fin:
            return {
                field: value
                for field, value in zip(['timestamp'] + REDDIT_POST_FIELDS, fin.readlines())
            }
