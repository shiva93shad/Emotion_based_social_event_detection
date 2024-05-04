import gensim
from sematch.semantic.similarity import WordNetSimilarity
import re
import math
import pymysql.cursors
from sematch.semantic.similarity import WordNetSimilarity

model = gensim.models.KeyedVectors.load_word2vec_format(
    "D:/all datasets/google_news_w2vec_model/GoogleNews-vectors-negative300.bin",
    binary=True,
)
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
cursor3 = cnx.cursor()

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

# compute li wordnet similarity
def w2vec_simCalculator(text_list):
    plutchik_list2 = []
    max_dic = {}
    for k, val in plutchik_wheel.items():
        max_val = 0
        for words in text_list:
            try:
                w2v_similarity = model.similarity(val, words)
                if w2v_similarity > max_val:
                    max_val = math.ceil(w2v_similarity * 100.0)
                # print("wup _ " + str(wup_similarity))
            except Exception as e:
                print(e)
                continue

        max_dic.update({k: max_val})
    plutchik_list2.extend(
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
    return plutchik_list2


# compute wordnet similarity using li method


def li_simCalculator(text_list):
    max_dic = {}
    plutchik_list = []
    for k, val in plutchik_wheel.items():
        max_val = 0
        for words in text_list:
            li_similarity = wns.word_similarity(val, words, "li")
            if li_similarity > max_val:
                max_val = math.ceil(li_similarity * 100.0)
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
    return plutchik_list


# alter1="ALTER TABLE emoji ADD LI VARCHAR(50) AFTER WUP;"
# cursor.execute(alter1)
#
# alter2="ALTER TABLE emoji ADD W2V VARCHAR(50) AFTER LI;"
# cursor.execute(alter2)

select = "SELECT id,keywordsNew From emoji "
# select="SELECT id,keywordsNew From emoji WHERE id >921"
cursor.execute(select)
resultset = cursor.fetchall()
description = []
i = 0

for row in resultset:
    id = row[0]
    kewords = row[1]
    kewords = re.sub("[^a-zA-Z]+", " ", kewords)
    text_list = kewords.split()

    li_list = li_simCalculator(text_list)
    update_tweet = "UPDATE emoji SET LI='%s' WHERE id='%s'" % (str(li_list), id)
    cursor2.execute(update_tweet)

    w2vec_list = w2vec_simCalculator(text_list)
    update_tweet2 = "UPDATE emoji SET W2V='%s' WHERE id='%s'" % (str(w2vec_list), id)
    cursor3.execute(update_tweet2)

    print(i)
    i += 1
    if i % 50 == 0:
        print("committed")
        cnx.commit()

cnx.commit()
cursor.close()
cursor2.close()
cnx.close()
