import csv
import pymysql
import pymysql.cursors

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
id_list = []
anger_list = []
fear_list = []
joy_list = []
sadness_list = []
sentiments = ["anger", "fear", "joy", "sadness"]
# table="facup"
table = "election"
sec = "100"
#
# file=open("../data/anger-fear_"+table+".txt","r",encoding="utf8")
# file2=open("../data/joy-sadness_"+table+".txt","r",encoding="utf8")
# reader=file.readlines()
# reader2=file2.readlines()
# for rows in reader:
#         id_list.append(rows.strip().split("\t")[0])
#         anger_list.append("{0:.1f}".format(round(float(rows.strip().split("\t")[1]),1))  )
#         fear_list.append("{0:.1f}".format(round(float(rows.strip().split("\t")[2]),1))  )
#         # print(anger_list)
#
# for row in reader2:
#         joy_list.append("{0:.1f}".format(round(float(row.strip().split("\t")[1]),1)))
#         sadness_list.append("{0:.1f}".format(round(float(row.strip().split("\t")[2]),1)))
#         # print(joy_list)
# file.close()
# file2.close()
#
# print(joy_list)
# count=0
# for items in id_list:
#     update=("UPDATE " + table + " "
#             "SET joy='%s' ,anger='%s',fear='%s',sadness='%s' WHERE id='%s'" % (joy_list[count], anger_list[count], fear_list[count], sadness_list[count], items))
#     cursor.execute(update)
#     count+=1
#     if count%30==0:
#         cnx.commit()
#         print("commited: "+str(count))
# cnx.commit()
#

select = "SELECT id,anger,fear,joy,sadness FROM " + table + " "
cursor.execute(select)
result = cursor.fetchall()

counter = 0
for rows in result:
    id = rows[0]
    anger = rows[1]
    fear = rows[2]
    joy = rows[3]
    sadness = rows[4]
    if float(joy) >= 0.5:
        joy = 1
    else:
        joy = 0

    if float(anger) >= 0.5:
        anger = 1
    else:
        anger = 0

    if float(fear) >= 0.5:
        fear = 1
    else:
        fear = 0

    if float(sadness) >= 0.5:
        sadness = 1
    else:
        sadness = 0

    update_tweet = (
        "UPDATE " + table + " "
        "SET joy6='%s' ,anger6='%s',fear6='%s',sadness6='%s' WHERE id='%s'"
        % (str(joy), str(anger), str(fear), str(sadness), id)
    )
    cursor2.execute(update_tweet)
    counter += 1
    if counter % 300 == 0:
        print("committed: " + str(counter))
        cnx.commit()
cnx.commit()


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
