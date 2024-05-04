import pymysql

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

table = "supertuesday"
# database="facupprocess"
sec = "120"
n = 3
threshold = 1.5
emotion_dict = ["anger", "fear", "joy", "sadness"]
timestamps = []

for item in emotion_dict:
    f = open(
        "../data/burst_results/" + table + "_" + item + "_" + sec + ".csv", mode="r"
    )
    i = 0
    id_list = []
    for line in f.readlines():
        if i == 0:
            i += 1
            continue
        # print(line.strip().split(','))
        # id_list.append(line.strip().split(',')[0])
        timestamps.append(line.strip().split(",")[1])

    f.close()
import datetime

dates = [
    datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in list(set(timestamps))
]
dates.sort()
sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d  %H:%M:%S") for ts in dates]
for row in sorteddates:
    print(row)
