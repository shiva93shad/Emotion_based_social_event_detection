import burst_detection as bd
import numpy as np
import pybursts

table = "supertuesday"
items = "joy"
sec = 3000
f = open(
    "../data/burst_results/" + table + "_" + items + "_" + str(sec) + ".txt",
    mode="r",
    encoding="utf8",
    newline="\n",
)
counter = 1
id = []
emotionCount = []
recordCount = []
time = []
for lines in f.readlines():
    id.append(counter)
    time.append((lines.strip().split("\t")[0]))
    recordCount.append(int(lines.strip().split("\t")[2]))
    emotionCount.append(int(lines.strip().split("\t")[3]))
    counter += 1

print((recordCount))
print((emotionCount))
f.close()

offset_list = []
cnt = 0
for items in emotionCount:
    offset_list.append(float(items / recordCount[cnt]))
    cnt += 1

# number of target events at each time point
r = np.array(emotionCount, dtype=float)
# total number of events at each time point
d = np.array(recordCount, dtype=float)
print(len(r))
print(len(d))
# number of time points
n = len(r)

# find the optimal state sequence (q)
q, d, r, p = bd.burst_detection(r, d, n, s=2, gamma=1, smooth_win=1)

# enumerate bursts based on the optimal state sequence
bursts = bd.enumerate_bursts(q, "burstLabel")

# find weight of bursts
weighted_bursts = bd.burst_weights(bursts, r, d, p)

print("observed probabilities: ")
print(str(r / d))

print("optimal state sequence: ")
print(str(q.T))

print("baseline probability: " + str(p[0]))

print("bursty probability: " + str(p[1]))

print("weighted bursts:")
print(weighted_bursts)

# offsets = [4, 17, 23, 27, 33, 35, 37, 76, 77, 82, 84, 88, 90, 92]
# print (pybursts.kleinberg(emotionCount, s=2, gamma=0.1))
