import pymysql
import scipy
import scipy.stats
import math

from sklearn import preprocessing


def pearson_correlations(numbers_x, numbers_y):
    mean_x = sum(numbers_x) / len(numbers_x)
    mean_y = sum(numbers_y) / len(numbers_y)

    subtracted_mean_x = [i - mean_x for i in numbers_x]
    subtracted_mean_y = [i - mean_y for i in numbers_y]

    x_times_y = [a * b for a, b in list(zip(subtracted_mean_x, subtracted_mean_y))]

    x_squared = [i * i for i in numbers_x]
    y_squared = [i * i for i in numbers_y]

    return sum(x_times_y) / math.sqrt(sum(x_squared) * sum(y_squared))


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
# cursor3 = cnx.cursor()
wheel = ["anger", "fear", "joy", "sadness"]

# 43	99
# 21	65
# 25	79
# 42	75
# 57	87
# 59	81
x = [43, 21, 25, 42, 57, 59]
y = [99, 65, 79, 75, 87, 81]


for item in wheel:

    select = (
        "SELECT intensity,TransEmotion,TWUP,TLI,TW2V,id FROM " + item + " LIMIT 100"
    )
    cursor.execute(select)
    result = cursor.fetchall()
    intensity_list = []
    emotion_list = []
    twup = []
    tw2v = []
    tli = []

    data_dic = {}
    wup_dict = {}
    for row in result:
        id = row[5]
        # print(int(row[2])/100)
        intensity_list.append(row[0])
        emotion_list.append(row[1])
        twup.append(float(row[2]))
        tli.append(float(row[3]))
        tw2v.append(float(row[4]))

        data_dic[id] = [row[0]]
        data_dic[id].append(row[1])

        wup_dict[id] = [row[0]]
        wup_dict[id].append(float(row[2]))
    # print(twup)
    # print(intensity_list)
    # print(emotion_list)
    gold_scores = []
    pred_scores = []
    gold_scores_range_05_1 = []
    pred_scores_range_05_1 = []
    sum_iee = 0
    sum_wup = 0
    wup_gold_scores = []
    wup_pred_scores = []
    wup_gold_scores_range_05_1 = []
    wup_pred_scores_range_05_1 = []

    for id in data_dic:
        if len(data_dic[id]) == 2:
            gold_scores.append(data_dic[id][0])
            pred_scores.append(data_dic[id][1])
            sum_iee += abs(data_dic[id][0] - data_dic[id][1])

            if data_dic[id][0] >= 0.5:
                gold_scores_range_05_1.append(data_dic[id][0])
                pred_scores_range_05_1.append(data_dic[id][1])

    for id in wup_dict:
        if len(data_dic[id]) == 2:
            wup_gold_scores.append(wup_dict[id][0])
            wup_pred_scores.append(wup_dict[id][1])
            sum_wup += abs(wup_dict[id][0] - wup_dict[id][1])

            if data_dic[id][0] >= 0.5:
                wup_gold_scores_range_05_1.append(wup_dict[id][0])
                wup_pred_scores_range_05_1.append(wup_dict[id][1])

    pearson_correlation = scipy.stats.pearsonr(gold_scores, pred_scores)
    # pearson_correlation2 = pearson_correlations(gold_scores, pred_scores)

    pearson_correlation_05_1 = scipy.stats.pearsonr(
        gold_scores_range_05_1, pred_scores_range_05_1
    )
    # pearson_correlation_05_1_2 = pearson_correlations(gold_scores_range_05_1, pred_scores_range_05_1)

    wup_pearson_correlation1 = scipy.stats.pearsonr(wup_gold_scores, wup_pred_scores)
    wup_pearson_correlation_05_1 = scipy.stats.pearsonr(
        wup_gold_scores_range_05_1, wup_pred_scores_range_05_1
    )

    # li_pearson_correlation = scipy.stats.pearsonr(emotion_list, tli)
    li_pearson_correlation = scipy.stats.pearsonr(intensity_list, tli)
    wup_pearson_correlation = scipy.stats.pearsonr(intensity_list, twup)
    w2v_pearson_correlation = scipy.stats.pearsonr(intensity_list, tw2v)
    print("\nsimple correlation by IEEE transaction:")
    print(item + ":" + str(pearson_correlation))

    print("\nsimple range 0.5-1  correlation by IEEE transaction:")
    print(item + ":" + str(pearson_correlation_05_1))

    # print("\nsimple correlation by wup similarity:")
    # print(item + ":" + str(wup_pearson_correlation1))
    #
    # print("\nsimple range 0.5-1  correlation by wup similarity:")
    # print(item + ":" + str(wup_pearson_correlation_05_1))

    print("\nsum of IEEE: " + str(sum_iee))
    print("\nsum of WUP: " + str(sum_wup))

    print("\nscipy x, y correlation: ", str(scipy.stats.pearsonr(x, y)))
    print("\nmy method x, y correlation: ", str(pearson_correlations(x, y)))

    # print("wordnet wup similarity :")
    # print(item + ":" + str(wup_pearson_correlation))
    #
    # print("wordnet li similarity :")
    # print(item + ":" + str(li_pearson_correlation))
    #
    # print("word embeding w2vec similarity :")
    # print(item + ":" + str(w2v_pearson_correlation))
    #
    import scipy.stats as stats

    print(stats.normaltest(gold_scores))
    print(stats.normaltest(gold_scores_range_05_1))
    print(stats.normaltest(pred_scores_range_05_1))
    # print(stats.spearmanr(gold_scores,pred_scores))
    # print(stats.spearmanr(wup_gold_scores, wup_pred_scores))
    from sklearn.metrics import r2_score

    print(r2_score(gold_scores, pred_scores, multioutput="variance_weighted"))
    print(r2_score(wup_gold_scores, wup_pred_scores, multioutput="variance_weighted"))
    from sklearn.metrics import mean_absolute_error
    from sklearn.metrics import r2_score

    y_true = gold_scores
    y_pred = pred_scores
    y2_pred = wup_pred_scores
    # r2_score(y_true, y_pred)
    print("mean absolute error : " + str(mean_absolute_error(y_true, y_pred)))
    print("mean absolute error wup: " + str(mean_absolute_error(y_true, y2_pred)))

    import numpy as np
    from sklearn.metrics import precision_recall_curve
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import explained_variance_score

    print("mean_squared_error : " + str(mean_squared_error(y_true, y_pred)))
    print("mean_squared_error wup: " + str(mean_squared_error(y_true, y2_pred)))
    # y_true = np.array(y_true)
    # y_pred = np.array(y_pred)
    # y2_pred = np.array(y2_pred)
    # # precision, recall, threshold = precision_recall_curve(y_true, y_scores)
    #
    # print("precision : " + str(average_precision_score(y_true, y_pred)))
    # print("precision wup: " + str(average_precision_score(y_true, y2_pred)))
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import r2_score

    scaler = StandardScaler()
    min_max_scaler = preprocessing.MinMaxScaler()
    # X_train_minmax = min_max_scaler.fit_transform()
    print(y_true)
    y_true = min_max_scaler.fit_transform(np.array(y_true))
    print(y_true)
    y_pred = min_max_scaler.fit_transform(y_pred)
    y2_pred = min_max_scaler.fit_transform(y2_pred)
    # print(y2_pred)
    # # r2_score(y_true, y_pred)
    print("r2_score : " + str(r2_score(y_true, y_pred)))
    print("r2_score wup: " + str(r2_score(y_true, y2_pred)))

# print(stats.normaltest(pred_scores))
