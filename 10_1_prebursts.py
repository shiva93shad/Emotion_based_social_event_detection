import csv
import pymysql
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
id_list = []
anger_list = []
fear_list = []
joy_list = []
sadness_list = []
sentiments = ["anger", "fear", "joy", "sadness"]
table = "supertuesday"
sec = "300"

for items in sentiments:
    f = open(
        "../data/burst_results/" + table + "_" + items + "_" + sec + ".txt",
        mode="w",
        encoding="utf8",
        newline="\n",
    )
    select_tweet_min = (
        "SELECT  publicationTime,GROUP_CONCAT(DISTINCT tags SEPARATOR ', '),COUNT(*) AS cnt, "
        "SUM(CASE WHEN " + items + "6=1 THEN 1 ELSE 0 END) AS cnt2 "
        "FROM " + table + " "
        "GROUP BY UNIX_TIMESTAMP(publicationTime) DIV %s "
        "ORDER BY publicationTime ASC ;" % (sec)
    )
    cursor.execute(select_tweet_min)
    re = cursor.fetchall()
    for line in re:
        f.write(
            str(line[0])
            + "\t"
            + str(line[1])
            + "\t"
            + str(line[2])
            + "\t"
            + str(line[3])
            + "\n"
        )
    f.close()


cnx.close
