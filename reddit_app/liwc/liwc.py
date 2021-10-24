import reddit_app.sql.model as model
from liwc_cols_with_nums import LIWC_NUM_TO_EMOTION

def make_insert_row_word(word, emotion_num_list) -> str:
    emotion_list = [LIWC_NUM_TO_EMOTION[num] for num in emotion_num_list]

    row_str = f"INSERT INTO regex_to_emotion (regex, is_regex, {', '.join(emotion_list)}) "
    row_str += f"VALUES (\"{word}\", {', '.join(['1'] * len(emotion_list))})"

    return row_str


# a function to try to find a regex matching a word if word is novel
# returns a dict of emotions to whether this word contains them
# if no match, returns and inserts no emotion
def match_regex(word: str):
    db_conn = model.get_db()

    result = db_conn.execute(f"SELECT * FROM regex_to_emotion WHERE regex = '{word}'").fetchone()
    
    while word != "":
        if result is not None:
            del result['regex']
            del result['is_regex']

            db_conn.execute(f"INSERT INTO word_to_emotion (word, {', '.join(result.keys())}) "
                            f"VALUES (\"{word}\", {', '.join(result.values())})")
            db_conn.commit()
            db_conn.close()
            return result

        word = word[:-1]
        result = db_conn.execute(f"SELECT * FROM regex_to_emotion WHERE regex = '{word}' AND is_regex = 1").fetchone()

    db_conn.execute(f"INSERT INTO word_to_emotion (word) VALUES (\"{word}\")")
    db_conn.commit()
    db_conn.close()

    return {emotion: 0 for emotion in LIWC_NUM_TO_EMOTION}

# a function to get list of emotions present in a word
def match_word(word: str):
    db_conn = model.get_db()
    result = db_conn.execute(f"SELECT * FROM word_to_emotion WHERE word = '{word}'").fetchone()
    db_conn.close()

    if result is not None:
        del result[word]
    else:
        result = match_regex(word)

    return result

# a function to get whether a specific emotion is present in a word
def word_has_emotion(word: str, emotion: str) -> bool:
    return match_word(word).get(emotion, 0) != 0