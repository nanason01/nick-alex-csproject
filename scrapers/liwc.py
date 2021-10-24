import sqlite3

LIWC_EMOTIONS_FILE = 'liwc_data/liwc_emotions.txt'
LIWC_WORDS_DICT_FILE = 'liwc_data/LIWC2015_English.txt'

def get_emotions():
    emotions_dict = {}

    with open(LIWC_EMOTIONS_FILE, 'r') as emotions_in:
        for line in emotions_in.readlines():
            num = int(line.split()[0])
            emotion = '_'.join(line.split()[1:])

            # further processing of emotion
            emotion = emotion.split('(')[1]
            emotion = emotion[:-1]

            emotions_dict[num] = emotion

    return emotions_dict

def create_liwc_table_cmd(emotions_dict):
    # emotion_to_num table
    print("CREATE TABLE emotion_to_num( ")
    print("emotion TEXT, ")
    print("num INTEGER NOT NULL, ")
    print("PRIMARY KEY (emotion) ")
    print(");")

    # regex_to_emotion table
    print("CREATE TABLE regex_to_emotion( ")
    print("regex TEXT, ")
    print("is_regex INTEGER NOT NULL, ")
    for emotion in emotions_dict.values():
        print(f"{emotion} INTEGER DEFAULT 0, ")
    print("PRIMARY KEY (regex) ")
    print(");")

    # word_to_emotion table
    print("CREATE TABLE word_to_emotion( ")
    print("word TEXT, ")
    for emotion in emotions_dict.values():
        print(f"{emotion} INTEGER DEFAULT 0, ")
    print("PRIMARY KEY (word) ")
    print(");")

def make_insert_row_regex(emotions_dict, regex, emotion_num_list) -> str:
    is_regex = regex[-1] == '*'
    if is_regex:
        regex = regex[:-1]
    
    emotion_list = [emotions_dict[num] for num in emotion_num_list]

    row_str = f"INSERT INTO regex_to_emotion (regex, is_regex, {', '.join(emotion_list)}) "
    row_str += f"VALUES (\"{regex}\", {'1' if is_regex else '0'}, {', '.join(['1'] * len(emotion_list))})"

    return row_str

def insert_regexes(db_conn, emotions_dict):
    with open(LIWC_WORDS_DICT_FILE, 'r') as dict_in:
        for line in dict_in.readlines():
            regex = line.split('\t')[0]
            emotion_num_list = [int(i) for i in line.split('\t')[1:]]

            task = make_insert_row_regex(emotions_dict, regex, emotion_num_list)
            print(task)
            db_conn.execute(task)
            
db_conn = sqlite3.connect("/mnt/c/Users/nicka/Desktop/nick-alex-csproject/reddit_app/sql/sqlite_db")

emotions_dict = get_emotions()

# create_liwc_table_cmd(emotions_dict)

# insert_regexes(db_conn, emotions_dict)

db_conn.commit()
db_conn.close()