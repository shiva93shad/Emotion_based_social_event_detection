import ast
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
# anger=row[0]
# fear=row[2]
# joy=row[3]
# sadness=row[4]
# #
################ adding to our table some columns  #####################
#
# ######################################################################
# for items in wheel:
#     alter=("ALTER TABLE "+items+" "
#     "ADD COLUMN mixed_wup VARCHAR(30) NOT NULL, "
#     "ADD COLUMN mixed_li VARCHAR(30) NOT NULL, "
#    "ADD COLUMN mixed_w2v VARCHAR(30) NOT NULL AFTER W2V")
#     cursor.execute(alter)

######################## retreive all emojis from db ###################
selection = "SELECT unicoded,WUP,LI,W2V FROM emoji "
cursor2.execute(selection)
res = cursor2.fetchall()
emoji_li = {}
emoji_wup = {}
emoji_w2v = {}
for row in res:
    emoji_li.update({row[0]: ast.literal_eval(row[2])})
    emoji_wup.update({row[0]: ast.literal_eval(row[1])})
    emoji_w2v.update({row[0]: ast.literal_eval(row[3])})
# print(emoji_li)
# print(emoji_wup)

########################################################################
for x_item in wheel:
    print(x_item)
    selection = "SELECT id,emoji FROM " + x_item + " "
    cursor.execute(selection)
    result = cursor.fetchall()
    emoji_dict = {}

    for item in result:
        emoji_list = []
        id = item[0]
        emoji_list = set(
            ast.literal_eval(item[1])
        )  # convert string list to actual python list
        if "" not in emoji_list:
            # print(emoji_list)
            emoji_dict.update({id: list(emoji_list)})

    counter = 0

    for k, v in emoji_dict.items():

        wup = []
        li = []
        w2v = []

        for i in v:
            i = "'" + i + "'"
            print((i))
            # print("yeeeeeeeeeeeeeeeeeeeeeeee")
            for ke, row in emoji_wup.items():
                # print(ke)
                if ke == (i):  # if you find that emoji on eemoji list
                    # print("yeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                    if x_item == "anger":
                        wup.append(
                            row[0] / 100
                        )  # according to order mentioned in emotion_dict
                    if x_item == "fear":
                        wup.append(row[2] / 100)
                    if x_item == "joy":
                        wup.append(row[3] / 100)
                    if x_item == "sadness":
                        wup.append(row[4] / 100)

            for ke, row in emoji_li.items():
                if ke == i:  # if you find that emoji on emoji list
                    if x_item == "anger":
                        li.append(
                            row[0] / 100
                        )  # according to order mentioned in emotion_dict
                    if x_item == "fear":
                        li.append(row[2] / 100)
                    if x_item == "joy":
                        li.append(row[3] / 100)
                    if x_item == "sadness":
                        li.append(row[4] / 100)

            for ke, row in emoji_w2v.items():
                if ke == i:  # if you find that emoji on emoji list
                    if x_item == "anger":
                        w2v.append(
                            row[0] / 100
                        )  # according to order mentioned in emotion_dict
                    if x_item == "fear":
                        w2v.append(row[2] / 100)
                    if x_item == "joy":
                        w2v.append(row[3] / 100)
                    if x_item == "sadness":
                        w2v.append(row[4] / 100)

        ##########################################commit update to db #######################################

        update_tweet = (
            "UPDATE " + x_item + " "
            "SET WUP='%s' ,LI='%s',W2V='%s' WHERE id='%s'"
            % (str(wup), str(li), str(w2v), k)
        )

        cursor2.execute(update_tweet)
        counter += 1
        if counter % 50 == 0:
            print(str(counter) + " : committed")
            cnx.commit()

cnx.commit()
cnx.close()
