# First we should filter input_array so that it does not contain NaN or Inf.
import numpy as np
import pymysql.cursors
import ast

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
float_formatter = lambda x: "%.2f" % x

# alter1="ALTER TABLE emoji ADD NLI VARCHAR(50) AFTER LI;"
# cursor.execute(alter1)
# alter2="ALTER TABLE emoji ADD NWUP VARCHAR(50) AFTER WUP;"
# cursor.execute(alter2)
# alter3="ALTER TABLE emoji ADD NW2V VARCHAR(50) AFTER W2V;"
# cursor.execute(alter3)

np.set_printoptions(formatter={"float_kind": float_formatter})

select = "SELECT WUP,LI,W2V,id FROM emoji "
cursor2.execute(select)

result = cursor2.fetchall()
for row in result:
    id = row[3]
    input_array_wup = np.array(ast.literal_eval(row[0]))
    input_array_li = np.array(ast.literal_eval(row[1]))
    input_array_w2v = np.array(ast.literal_eval(row[2]))
    # sum of the numpy array should be 1 , normalization between 0 and 1
    nwup = list(input_array_wup / input_array_wup.sum(axis=0, keepdims=1))
    # print(nwup.tolist())
    nwup = [round(float(i), 2) for i in nwup]
    print(nwup)
    nli = list(input_array_li / input_array_li.sum(axis=0, keepdims=1))
    # print(nli.tolist())
    nli = [round(float(i), 2) for i in nli]
    print(nli)
    nw2v = list(input_array_w2v / input_array_w2v.sum(axis=0, keepdims=1))

    nw2v = [round(float(i), 2) for i in nw2v]
    print(nw2v)
    update_tweet = "UPDATE emoji " "SET NWUP='%s',NLI='%s',NW2V='%s'  WHERE id='%d'" % (
        (nwup),
        (nli),
        (nw2v),
        id,
    )
    # ("UPDATE tblTableName SET Year=%s, Month=%s, Day=%s, Hour=%s, Minute=%s WHERE Server='%s' " % (Year, Month, Day, Hour, Minute, ServerID)
    cursor.execute(update_tweet)
cnx.commit()
