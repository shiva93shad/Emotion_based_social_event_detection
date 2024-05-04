import ast
import numpy as np
import math
import pymysql.cursors

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
wheel = ["anger", "fear", "joy", "sadness"]
emotion_dict = [
    "Anger",
    "Disgust",
    "Fear",
    "Joy",
    "Sadness",
    "Surprise",
    "Trust",
    "Anticipation",
]

##################################################################################


def min_max_median_mean(TransEmotion, WUP, intensity):
    statistic = []
    # first method
    if len(WUP) == 1:
        if TransEmotion >= WUP[0]:
            min1 = WUP[0]
            max1 = TransEmotion
        else:
            max1 = WUP[0]
            min1 = TransEmotion

        avg = (TransEmotion + WUP[0]) / 2
        avg = math.ceil(avg * 100.0) / 100.0

    else:
        min_wup = min(WUP)
        max_wup = max(WUP)
        i = 0
        sum1 = 0
        for j in WUP:
            sum1 += j
            i += 1
        avg_wup = sum1 / i

        if TransEmotion >= avg_wup:
            min1 = min_wup
            max1 = TransEmotion
        else:
            max1 = max_wup
            min1 = TransEmotion

        avg = (TransEmotion + WUP[0]) / 2
        avg = math.ceil(avg * 100.0) / 100.0

    statistic.append(min1)
    statistic.append(max1)
    statistic.append(avg)
    return statistic


#######################################################

# second method
# if intensity < TransEmotion:
#######################################################


def nullremover(x):
    return x if x is not None else 0


####################### main program ##################
count = 0
for items in wheel:
    print(items)
    select = (
        "SELECT TransEmotion,WUP,LI,W2V,intensity,id,emojiCount  FROM " + items + " "
    )
    cursor.execute(select)
    result = cursor.fetchall()
    counter = 0

    for row in result:
        # mixed list in order is
        mixed_wup = []
        mixed_w2c = []
        mixed_li = []

        TransEmotion = row[0]
        WUP = row[1]
        # print(WUP)
        LI = row[2]
        W2V = row[3]
        intensity = row[4]
        id = row[5]
        emoji_count = row[6]

        if emoji_count == 0:

            mixed_wup.append(TransEmotion)
            mixed_li.append(TransEmotion)
            mixed_w2c.append(TransEmotion)

        else:
            # print(WUP)
            WUP = ast.literal_eval(WUP)
            wup = min_max_median_mean(TransEmotion, WUP, intensity)
            wup_min = wup[0]
            wup_max = wup[1]
            wup_avg = wup[2]
            mixed_wup.extend([wup_min, wup_max, wup_avg])

            LI = ast.literal_eval(LI)
            li = min_max_median_mean(TransEmotion, LI, intensity)
            li_min = li[0]
            li_max = li[1]
            li_avg = li[2]
            mixed_li.extend([li_min, li_max, li_avg])

            W2V = ast.literal_eval(W2V)
            w2v = min_max_median_mean(TransEmotion, W2V, intensity)
            w2v_min = w2v[0]
            w2v_max = w2v[1]
            w2v_avg = w2v[2]
            mixed_w2c.extend([w2v_min, w2v_max, w2v_avg])

        update_tweet = (
            "UPDATE " + items + " "
            "SET mixed_w2v='%s' ,mixed_wup='%s',mixed_li='%s' WHERE id='%s'"
            % (str(mixed_w2c), str(mixed_wup), str(mixed_li), id)
        )

        cursor2.execute(update_tweet)
        counter += 1
        if counter % 50 == 0:
            print(str(counter) + " : committed")
            cnx.commit()
    cnx.commit()
cnx.commit()
cnx.close()
