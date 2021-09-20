import formats.wsb_post as wsb_post
import scrapers.reddit as reddit

poster = wsb_post.WSB_Post()

count = 0

while True:
    resp_json = reddit.reddit_get('https://oauth.reddit.com/r/wallstreetbets/new')

    for json_in in resp_json['data']['children']:
        poster.digest_json(json_in)

    count += resp_json['data']['dist']
    print('processed', count)