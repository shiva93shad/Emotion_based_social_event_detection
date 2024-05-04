import ast
import math
import re
import requests
import sys
from csv import writer
import unicodedata as ud
import string


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


import pymysql.cursors
import unicodedata

db = "emoji"
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
cursor2 = cnx.cursor()

all_emoji = "SELECT unicoded FROM emoji "
cursor2.execute(all_emoji)
emoji_results = cursor2.fetchall()
all_emoji_list = []
for i in emoji_results:
    all_emoji_list.append(i[0][2:-1])
    print(i[0])
print(all_emoji_list)

select = "SELECT emoji FROM twitter "
cursor.execute(select)
results = cursor.fetchall()
# ast.literal_eval(prescribe)[0]['keywords']  this is use to chamge string list to python list
emoji_list = []
missed_emoji = []
for items in results:

    li = ast.literal_eval(items[0])
    # print(li[2:])
    if "" in li:
        continue

    else:
        # search_emoji(li,all_emoji_list)

        for items in li:
            if str(items[1:]) in all_emoji_list:
                print("exist")

            else:
                print("not exist")
                missed_emoji.append(str(items[1:]))

print(missed_emoji)
print(set(missed_emoji))
# with open("../data/missed_emoji.txt", mode="w") as outfile:
#     for item in set(missed_emoji):
#         outfile.write(item + "\n")
#
