import gensim
import pymysql
from csv import reader, writer
from numba import vectorize
from numba import *

print("loading w2vec model :")
w2vecpath = "../neural networks/word2vec_twitter_model.bin"
w2vecpath = "../data/w2v_model_data.gm"
# load word2vec model, here GoogleNews is used
# model = gensim.models.KeyedVectors.load_word2vec_format(w2vecpath, binary=True)
model = gensim.models.Word2Vec.load(w2vecpath)
# model = gensim.models.KeyedVectors.load_word2vec_format(w2vecpath, binary=True,unicode_errors='ignore')


def w2vec_similarity(a, b):
    # calculate distance between two sentences using WMD algorithm
    # distance = model.wmdistance(a, b)
    distance = model.wv.n_similarity(a.split(), b.split())
    return distance


table = "facup"
database = "facupprocess"
sec = "80"
n = 3
threshold = 1.5
emotion_dict = ["anger", "fear", "joy", "sadness"]
# item='joy'


cnx = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="",
    db="emoji",
    charset="utf8",
    cursorclass=pymysql.cursors.SSCursor,
)
cursor = cnx.cursor()
cursor2 = cnx.cursor()


print("word 2 vec model loaded successfully!")

for item in emotion_dict:
    print(item)
    id_list = []
    timestamps = []
    f = open(
        "../data/burst_results/" + table + "_" + item + "_" + sec + ".csv", mode="r"
    )
    i = 0
    for line in f.readlines():
        if i == 0:
            i += 1
            continue
        # print(line.strip().split(','))
        # id_list.append(line.strip().split(',')[0])
        timestamps.append(line.strip().split(",")[1])
    import datetime

    dates = [datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps]
    dates.sort()
    sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d  %H:%M:%S") for ts in dates]
    print(sorteddates)
    w2vec_resluts = {}
    for items in sorteddates:
        cursor = cnx.cursor()
        select = (
            "SELECT cleanedText FROM "
            + table
            + " WHERE publicationTime BETWEEN '"
            + items
            + "' AND '"
            + items
            + "'+INTERVAL "
            + sec
            + " SECOND  "
        )
        cursor.execute(select)
        resultset = cursor.fetchall()
        print(resultset)
        count = 0
        # compare each two items in a list
        w2vec = []
        sum = 0
        for i in range(len(resultset)):
            for j in range(i + 1, len(resultset)):
                if resultset[i][0] == "" or resultset[j][0] == "":
                    print(resultset[i][0])
                    print(resultset[j][0])
                    print("error")
                    continue
                res = w2vec_similarity(resultset[i][0], resultset[j][0])
                w2vec.append(res)
                sum += float(res)
                count += 1
                if count % 10000 == 0:
                    print(count)

        avg_w2vec = float(sum / len(w2vec))
        print(avg_w2vec)
        w2vec_resluts.update({items: avg_w2vec})
        cursor.close()

    f.close()

    f2 = open(
        "../data/w2vec_results/w2vec_" + table + "_" + item + "_" + sec + ".csv",
        mode="w",
    )
    wr = writer(f2, delimiter=",")
    wr.writerow(["eventTime", "w2vec_similarity"])
    for k, v in w2vec_resluts.items():
        wr.writerow([k, v])

    f2.close()
