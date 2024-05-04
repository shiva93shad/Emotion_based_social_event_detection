import ast
import csv
import pymysql

db = "emoji"
dataset = "emoji"
cnx = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="root",
    db=db,
    charset="utf8",
    cursorclass=pymysql.cursors.SSCursor,
)
cursor = cnx.cursor()

with open("../data/emoji_description.csv", mode="r", newline="") as incsv:
    reader = csv.reader(incsv, delimiter=",")
    all_emojis = []
    # all_emojis.append(''.join(('\\',"U0001F32E")))
    # all_emojis.append("U0001F32E")
    emoji_dict = {}
    for row in reader:
        emoji = row[0]
        prescribe = row[1]
        emoji2 = int(emoji[1:], 16)
        k = chr(int(format(emoji2, "X"), 16)).encode("utf-8")
        k = k.decode("unicode-escape").encode("latin1").decode("utf8")
        asci = ascii(k)
        # print(k)
        all_emojis.append(k)
        keywords = ast.literal_eval(prescribe)[0]["keywords"]
        description = ast.literal_eval(prescribe)[0]["description"]
        title = ast.literal_eval(prescribe)[0]["title"]
        # print()
        insert_tweet = (
            "INSERT INTO " + dataset + " "
            "( unicoded, title, keywords, description ) "
            "VALUES (%(unicoded)s, %(title)s, %(keywords)s , %(description)s)"
        )
        tweet_data = {
            "unicoded": asci,
            "title": str(title),
            "keywords": str(keywords),
            "description": str(description),
        }
        # Insert new employee
        cursor.execute(insert_tweet, tweet_data)
    cnx.commit()
    # print(my_lst)


# with open("../data/emojipedia_all.csv", mode='a', newline='') as outcsv:
#     wr = writer(outcsv, delimiter=',')
#     wr.writerow(["unicode","title","EmojiRestApi" "description"])
# #
# with open("../data/emojipedia_all.csv",mode='a',newline='') as outcsv:
#     wr = writer(outcsv, delimiter=',')
#
#     for emoji,prescribe in emoji_dict.items():
#         codeprints=Emojipedia.search(emoji).codepoints
#         discription=Emojipedia.search(emoji).description
#         title=Emojipedia.search(emoji).title
#         # print(discription)
#         discription2 = re.sub('[^0-9a-zA-Z]+', ' ', discription)
#         print(title)
#         wr.writerow([ascii(emoji),title,prescribe,discription2])
#         print("success")
# break
cursor.close()
cnx.close()
