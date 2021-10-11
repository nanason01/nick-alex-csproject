
REDDIT_POSTS_DIR = 'reddit_posts'

REDDIT_POST_FIELDS = [
    'score',
    'upvote_ratio',
    'total_awards_received',
    'num_comments',
    'author',
    'title',
    'selftext',
]

PUSHSHIFT_LAST_TIMESTAMP_FILE = 'pushshift_last_timestamp_dont_delete'

SQLITE_DB_FILENAME = 'reddit_app/sql/sqlite_db'

SUBREDDIT_TO_INT = {
    'wallstreetbets': 1,
}
INT_TO_SUBREDDIT = {
    val: key
    for key, val in SUBREDDIT_TO_INT.items()
}