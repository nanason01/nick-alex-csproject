import sqlite3
from config import SQLITE_DB_FILENAME

db_conn = None

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    db_filename = SQLITE_DB_FILENAME
    db_conn = sqlite3.connect(str(db_filename))
    db_conn.row_factory = dict_factory

    # Foreign keys have to be enabled per-connection.  This is an sqlite3
    # backwards compatibility thing.
    db_conn.execute("PRAGMA foreign_keys = ON")

    return db_conn


def close_db(db_conn):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if db_conn is not None:
        db_conn.commit()
        db_conn.close()
