PRAGMA foreign_keys = ON;

CREATE TABLE posts(
    postid VARCHAR(8) NOT NULL,
    created_utc DATETIME NOT NULL,
    score FLOAT,
    upvote_ratio FLOAT,
    total_awards_received FLOAT,
    author VARCHAR(64) NOT NULL,
    subreddit INTEGER NOT NULL,
    title TEXT,
    selftext TEXT,
    PRIMARY KEY (postid, author, created_utc, subreddit)
);

CREATE TABLE stocks(
    symbol VARCHAR(8) NOT NULL,
    utc DATETIME NOT NULL,
    open_price FLOAT,
    close_price FLOAT,
    high FLOAT,
    low FLOAT,
    volume INTEGER,
    PRIMARY KEY (utc, symbol)
);