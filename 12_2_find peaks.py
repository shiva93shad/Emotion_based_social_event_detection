import pymysql.cursors
import pymysql
import pandas as pd
import numpy as np
import peakutils

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
selection = (
    "SELECT startTime,cnt,cnt2,avgcnt FROM superprocess WHERE emotionId='%s';" % ("joy")
)
cursor.execute(selection)
resultset = cursor.fetchall()
cnt = []
cnt2 = []
avgcnt = []
time = []
for items in resultset:
    time.append(items[0])
    cnt.append(items[1])
    cnt2.append(items[2])
    # print(cnt2)
    avgcnt.append(int(float(items[3]) * 100))
    print(avgcnt)
# cb = np.array([-0.010223, ... ])
cnt = np.array(cnt)
cnt2 = np.array(cnt2)
avg = np.array(avgcnt)

indexes1 = peakutils.indexes(cnt, thres=0.05 / max(cnt), min_dist=100)
print(indexes1)

for items in indexes1:
    print(time[items])
indexes2 = peakutils.indexes(cnt2, thres=0.05 / max(cnt2), min_dist=100)
print(indexes2)

for items in indexes2:
    print(time[items])
#
# indexes3 = peakutils.indexes(avgcnt, thres=0.02/max(avgcnt), min_dist=100)
# print(indexes3)
# for items in indexes3:a
#     print(time[items])
