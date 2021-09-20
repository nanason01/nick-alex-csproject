from datetime import datetime
import pathlib
import sys

from config import REDDIT_POST_FIELDS, WALLSTREETBETS_DIR

wsb_dirpath = pathlib.Path(WALLSTREETBETS_DIR)
wsb_dirpath.mkdir(exist_ok=True)

def utc_to_dt(timestampValue):
   # get the UTC time from the timestamp integer value.
   d = datetime.utcfromtimestamp( int(timestampValue) )

   # calculate time difference from utcnow and the local system time reported by OS
   offset = datetime.now() - datetime.utcnow()

   # Add offset to UTC time and return it
   return d + offset

class Pushshift_Post:
    # store a json as a file with proper placement and format
    def digest_json(self, json_in):
        created_utc = json_in['created_utc']
        created_datetime = utc_to_dt(created_utc)
        day_dir_str = str(created_datetime.date())
        
        day_dir = wsb_dirpath / day_dir_str
        day_dir.mkdir(exist_ok=True)

        post_id = json_in['id']
        out_file = day_dir / post_id

        with open(str(out_file), 'w') as fout:
            fout.write(str(created_datetime))
            fout.write('\n')

            fout.writelines([
                str(json_in.get(field, 'no field found')) + '\n'
                for field in REDDIT_POST_FIELDS
            ])

    # return a dict of important fields from a previously stored file
    # equivalent to the stripped 'data' field of the json_in
    def digest_file(self, filename):
        if not pathlib.Path(filename).exists():
            print('Error:', filename, 'does not exist', file=sys.stderr)
            return
        
        with open(filename, 'r') as fin:
            return {
                field: value
                for field, value in zip(['timestamp'] + REDDIT_POST_FIELDS, fin.readlines())
            }
