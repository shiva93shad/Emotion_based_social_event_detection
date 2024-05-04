import ast
import csv
import pymysql
from nltk.corpus import sentiwordnet as swn
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
import re
import ast
import itertools
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

db = "emoji"
dataset = "emoji"

stops = set(stopwords.words("english"))
stops.add("emoji")
stops.add("unicode")
stops.add("added")
stops.add("approved")
stops.add("emoji")
stops.add("under")
stops.add("part")
stops.add("name")

cnx = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="root",
    db=db,
    charset="utf8",
    cursorclass=pymysql.cursors.SSCursor,
)
cursor = cnx.cursor()

select = "SELECT id,keywords,description From emoji WHERE id<922"
cursor.execute(select)
res = cursor.fetchall()
description = []
i = 0
for row in res:
    myset = ()
    filtered_sentence = []
    id = row[0]
    keywords = ast.literal_eval(row[1])
    # print(keywords)
    keywords2 = [w.lower() for w in keywords if 1 == 1]
    sentence = row[2]
    sentence = re.sub("[^a-zA-Z]+", " ", sentence)
    # print(sentence)
    word_list = []
    filtered_sentence = [
        w.lower() for w in word_tokenize(sentence) if not w.lower() in stops
    ]

    myset = set(itertools.chain(keywords, filtered_sentence))
    # print(myset)
    for word in list(myset):
        # print(word)
        if (sid.polarity_scores(word)["compound"]) >= 0.1:
            word_list.append(word)
        elif (sid.polarity_scores(word)["compound"]) <= -0.1:
            word_list.append(word)

    new_keywords = list(set(itertools.chain(keywords2, word_list)))
    print(new_keywords)
    update_tweet = "UPDATE emoji " "SET keywordsNew='%s' WHERE id='%d'" % (
        " ".join(new_keywords),
        id,
    )
    # ("UPDATE tblTableName SET Year=%s, Month=%s, Day=%s, Hour=%s, Minute=%s WHERE Server='%s' " % (Year, Month, Day, Hour, Minute, ServerID)
    cursor.execute(update_tweet)
    i += 1
    print(i)
    if i % 100 == 0:
        cnx.commit()


cnx.commit()
cursor.close()
cnx.close()
