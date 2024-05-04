# this script is used for extract plutchik emotion intensities from emojis text
#
#
#
#


import re

import math
import pymysql.cursors
from sematch.semantic.similarity import WordNetSimilarity

wns = WordNetSimilarity()
cnx = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="root",
    db="emoji",
    charset="utf8",
    cursorclass=pymysql.cursors.SSCursor,
)
cursor = cnx.cursor()
cursor2 = cnx.cursor()
plutchik_wheel = {
    1: "Anger",
    2: "Disgust",
    3: "Fear",
    4: "Joy",
    5: "Sadness",
    6: "Surprise",
    7: "Trust",
    8: "Anticipation",
}
wheel = [
    "Anger",
    "Disgust",
    "Fear",
    "Joy",
    "Sadness",
    "Surprise",
    "Trust",
    "Anticipation",
]


def simCalculator(resultset):
    i = 0

    for row in resultset:
        # print(row)
        text_list = []
        id = row[0]
        kewords = row[1]
        kewords = re.sub("[^a-zA-Z]+", " ", kewords)
        text_list = kewords.split()
        print(text_list)

        max_dic = {}
        plutchik_list = []
        for k, val in plutchik_wheel.items():
            max_val = 0
            for words in text_list:
                wup_similarity = wns.word_similarity(val, words, "wup")
                if wup_similarity > max_val:
                    max_val = math.ceil(wup_similarity * 100.0)
                # print("wup _ " + str(wup_similarity))

            max_dic.update({k: max_val})
        plutchik_list.extend(
            (
                max_dic.get(1),
                max_dic.get(2),
                max_dic.get(3),
                max_dic.get(4),
                max_dic.get(5),
                max_dic.get(6),
                max_dic.get(7),
                max_dic.get(8),
            )
        )

        update_tweet = "UPDATE emoji SET WUP='%s' WHERE id='%s'" % (
            str(plutchik_list),
            id,
        )
        # ("UPDATE tblTableName SET Year=%s, Month=%s, Day=%s, Hour=%s, Minute=%s WHERE Server='%s' " % (Year, Month, Day, Hour, Minute, ServerID)
        cursor2.execute(update_tweet)
        i += 1
        print(i)
        if i % 100 == 0:
            cnx.commit()


select = "SELECT id,keywordsNew From emoji "
# select="SELECT id,keywordsNew From emoji WHERE id >921"
cursor.execute(select)
resultset = cursor.fetchall()
description = []
simCalculator(resultset)

cnx.commit()
cursor.close()
cursor2.close()
cnx.close()
