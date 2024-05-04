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

table = "facup"
database = "facupprocess"
sec = "80"
n = 3
threshold = 1.5
item = "joy"
f = open("../data/burst_results/" + table + "_" + item + "_" + sec + ".csv", mode="r")
i = 0
id_list = []
for line in f.readlines():
    if i == 0:
        i += 1
        continue
    # print(line.strip().split(','))
    id_list.append(line.strip().split(",")[0])
    # timestamps.append(line.strip().split(',')[1])

cnt = []
cnt2 = []
for items in id_list:
    cursor = cnx.cursor()
    select = "SELECT cnt,cnt2,startTime FROM " + database + " WHERE id= %s ;" % (items)
    cursor.execute(select)
    resultset = cursor.fetchall()
    for item in resultset:
        print(item)
    cnt.append(resultset[0][0])
    cnt2.append(resultset[0][1])

sum_cnt = 0
sum_cnt2 = 0

for it in cnt:
    sum_cnt += it
avg_cnt = float(sum_cnt / len(cnt))

for it2 in cnt2:
    sum_cnt2 += it2
avg_cnt2 = float(sum_cnt2 / len(cnt2))

print("cnt")
print(avg_cnt)


print("cnt2")
print(avg_cnt2)
# for row in cnt2 :
#     if row > avg_cnt2:
#         print(row)

f.close()
