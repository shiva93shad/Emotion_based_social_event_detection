import ast

import pymysql
import scipy
import scipy.stats

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
# cursor3 = cnx.cursor()
wheel = ["anger", "fear", "joy", "sadness"]

for item in wheel:

    select = (
        "SELECT intensity,mixed_w2v,mixed_wup,mixed_li,TransEmotion FROM "
        + item
        + " WHERE emojiCount>=1 "
    )
    cursor.execute(select)
    result = cursor.fetchall()
    intensity_list = []
    min_w2v_list = []
    max_w2v_list = []
    avg_w2v_list = []
    min_wup_list = []
    max_wup_list = []
    avg_wup_list = []
    min_li_list = []
    max_li_list = []
    avg_li_list = []
    trans_emotion = []
    for row in result:
        w2v_list = []
        wup_list = []
        li_list = []
        trans_emotion.append(row[4])
        intensity_list.append(row[0])
        w2v_list = ast.literal_eval(row[1])

        if len(w2v_list) == 1:
            min_w2v_list.append(w2v_list[0])
            max_w2v_list.append(w2v_list[0])
            avg_w2v_list.append(w2v_list[0])

        else:
            min_w2v_list.append(w2v_list[0])
            max_w2v_list.append(w2v_list[1])
            avg_w2v_list.append(w2v_list[2])

        wup_list = ast.literal_eval(row[2])

        if len(wup_list) == 1:
            min_wup_list.append(wup_list[0])
            max_wup_list.append(wup_list[0])
            avg_wup_list.append(wup_list[0])
        else:
            min_wup_list.append(wup_list[0])
            max_wup_list.append(wup_list[1])
            avg_wup_list.append(wup_list[2])

        li_list = ast.literal_eval(row[3])

        if len(li_list) == 1:
            min_li_list.append(li_list[0])
            max_li_list.append(li_list[0])
            avg_li_list.append(li_list[0])
        else:
            min_li_list.append(li_list[0])
            max_li_list.append(li_list[1])
            avg_li_list.append(li_list[2])
        # emotion_list.append(row[1])
    pc_min_w2v = scipy.stats.pearsonr(intensity_list, min_w2v_list)
    pc_max_w2v = scipy.stats.pearsonr(intensity_list, max_w2v_list)
    pc_avg_w2v = scipy.stats.pearsonr(intensity_list, avg_w2v_list)

    pc_min_wup = scipy.stats.pearsonr(intensity_list, min_wup_list)
    pc_max_wup = scipy.stats.pearsonr(intensity_list, max_wup_list)
    pc_avg_wup = scipy.stats.pearsonr(intensity_list, avg_wup_list)

    pc_min_li = scipy.stats.pearsonr(intensity_list, min_li_list)
    pc_max_li = scipy.stats.pearsonr(intensity_list, max_li_list)
    pc_avg_li = scipy.stats.pearsonr(intensity_list, avg_li_list)
    print(item)
    print("pc_min_li : " + str(pc_min_li))
    print("pc_max_li : " + str(pc_max_li))
    print("pc_avg_li : " + str(pc_avg_li))

    print("pc_min_wup : " + str(pc_min_wup))
    print("pc_max_wup : " + str(pc_max_wup))
    print("pc_avg_wup : " + str(pc_avg_wup))

    print("pc_min_w2v : " + str(pc_min_w2v))
    print("pc_max_w2v : " + str(pc_max_w2v))
    print("pc_avg_w2v : " + str(pc_avg_w2v))
