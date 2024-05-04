import requests

# '[\U0001F602-\U0001F64F]'
# \U0001F000-\U0001FFFF
import sys
from csv import writer
import unicodedata as ud
import string
import re


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


start = int("0001F000", 16)
end = int("0001FFFF", 16)


printable = set(string.printable)
twitter_emoji = []
# add all twitter emojis into a list to decode it later
for i in range(start, end + 1):
    # print(chr(int(format(i, 'X'), 16)).encode('utf-8'))

    k = chr(int(format(i, "X"), 16)).encode("utf-8")
    k = k.decode("unicode-escape").encode("latin1").decode("utf8")
    asci = ascii(k)

    asci = re.sub("[^0-9a-zA-Z]+", "", asci)
    print(asci)
    twitter_emoji.append(asci)

counter = 0
all_counter = 0
with open("../data/emoji_description.csv", "a", newline="") as outcsv:
    wr = writer(outcsv)
    for items in twitter_emoji:
        resp = requests.get("http://emojinet.knoesis.org/api/emoji/" + items + "")
        # print('http://emojinet.knoesis.org/api/emoji/'+items+'')
        jsonRes = resp.json()
        if resp.status_code != 200:
            # This means something went wrong.
            # print(resp.json())
            # raise APIError('GET /tasks/ {}'.format(resp.status_code))
            print("no such emmoji exists...")
            continue

        else:
            all_counter += 1
            print("all succesful requests: " + str(all_counter))
            if not jsonRes:
                counter += 1
                print("empty succesful requests: " + str(counter))
            else:
                wr.writerow([items, resp.json()])  # writes title row
