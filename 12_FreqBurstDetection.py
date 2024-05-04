# in this algorithm we use frequency based event detection of thelwal and paltoghlou method in 2011
from csv import writer
import pymysql.cursors

# cnx = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='euro2016', charset='utf8',cursorclass = pymysql.cursors.SSCursor)
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
cursor3 = cnx.cursor()
# table="facup"
# database2="facupprocess"
table = "supertuesday"
database2 = "superprocess"
# parameters to be set
# sec=60 for semifrequency table
# for semifrequency2 table
sec = "80"
n = 3
threshold = 1.5
emotion_dict = ["anger", "fear", "joy", "sadness"]

# ################################################################
def tokenSpikes(item, ids):
    i = 1
    em_dict = {}
    event_list = []
    print(item)
    print(ids)
    # exit()
    with open(
        "../data/burst_results/" + table + "_" + item + "_" + sec + ".csv",
        "w",
        newline="",
    ) as outcsv:
        wr = writer(outcsv, delimiter=",")
        wr.writerow(["id", "eventTime", "avgerageCnt"])  # writes title row
        for val in ids.keys():

            # extract just one tweet by id
            frequency = (
                "SELECT cnt,cnt2,startTime,avgcnt FROM "
                + database2
                + " WHERE id = %s ;" % (val)
            )
            cursor.execute(frequency)
            res = list(cursor.fetchone())
            all_freq = res[0]
            freq = res[1]
            startTime = res[2]
            avgcnt = res[3]
            # extract average of 3 window B4 that
            if i == 1:
                avgSelection = (
                    "SELECT cnt2, cnt FROM " + database2 + " WHERE id = %s ;" % (val)
                )
                i += 1
            elif i == 2:
                avgSelection = (
                    "SELECT AVG(t.cnt2) AS the_average, AVG(t.cnt) AS avgCnt "
                    "FROM (SELECT cnt2,cnt FROM "
                    + database2
                    + " WHERE id < %s ORDER BY id DESC LIMIT %s )t;" % (val, i - 1)
                )
                i += 1
            elif i == 3:
                avgSelection = (
                    "SELECT AVG(t.cnt2) AS the_average , AVG(t.cnt) AS avgCnt "
                    "FROM (SELECT cnt2,cnt FROM "
                    + database2
                    + " WHERE id < %s ORDER BY id DESC LIMIT %s )t;" % (val, i - 1)
                )
                i += 1
            else:
                avgSelection = (
                    "SELECT AVG(t.cnt2) AS the_average , AVG(t.cnt) AS avgCnt "
                    "FROM (SELECT cnt2,cnt FROM "
                    + database2
                    + " WHERE id < %s ORDER BY id DESC LIMIT %s )t;" % (val, n)
                )
                i += 1
            cursor2.execute(avgSelection)
            res = list(cursor2.fetchone())
            Avg = res[0]
            print(res)
            avg_all = res[1]
            avgCount = float(Avg / avg_all)
            print("avg:" + str(Avg))
            # print(all_freq)
            if float(freq) >= float(threshold) * float(Avg):
                wr.writerow([val, startTime, float(avgcnt)])
                event_list.append(startTime)

        em_dict.update({item: event_list})

    return em_dict


# SELECT avg(t.NegFreq) FROM (SELECT NegFreq FROM tk2 WHERE id<='%s' ORDER BY id DESC LIMIT 2) t ;" % i[0]
################################################################
def frequencyDetector():
    for items in emotion_dict:
        select_tweet_min = (
            "SELECT  id,publicationTime,GROUP_CONCAT(DISTINCT tags SEPARATOR ', '),COUNT(*) AS cnt, "
            "SUM(CASE WHEN " + items + "6=1 THEN 1 ELSE 0 END) AS cnt2  "
            "FROM " + table + " "
            # " WHERE  publicationTime between '2012-05-05 16:00:00' and '2012-05-05 18:10:00' "
            "GROUP BY  FLOOR(UNIX_TIMESTAMP(publicationTime)/ %s ) "
            "ORDER BY publicationTime ASC ;" % (sec)
        )

        cursor.execute(select_tweet_min)
        result_set = cursor.fetchall()
        insert_tweet = (
            "INSERT INTO " + database2 + " "
            "(emotionId, startTime, hashtag, cnt ,cnt2, avgcnt ) "
            "VALUES (%(emotionId)s, %(startTime)s, %(hashtag)s, %(cnt)s, %(cnt2)s, %(avgcnt)s) "
        )

        for row in result_set:
            tweet_data = {
                "emotionId": items,
                "startTime": row[1],
                "hashtag": row[2],
                "cnt": row[3],
                "cnt2": row[4],
                "avgcnt": ("{0:.2f}".format(round((row[4] / row[3]), 2))),
            }
            cursor2.execute(insert_tweet, tweet_data)
        cnx.commit()


##################################################################

truncate = "Truncate " + database2 + " "
cursor.execute(truncate)
frequencyDetector()
package_list = []
for item in emotion_dict:
    select = (
        "SELECT id,startTime FROM " + database2 + " WHERE emotionId='%s' ;" % (item)
    )
    cursor3.execute(select)
    results = cursor3.fetchall()
    print((results))
    # exit()
    ids = {}
    for row in results:
        ids.update({row[0]: row[1]})
    li = tokenSpikes(item, ids)
    package_list.append(li)

for items in package_list:
    print(items.keys())
    print("event times:")
    print(items.values())


cursor2.close()
cursor3.close()
cursor.close()
cnx.close()
