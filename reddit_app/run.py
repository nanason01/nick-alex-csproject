import dash

import reddit_app
from reddit_app.app import app

if __name__ == '__main__':
    app.run_server(debug=True)