#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import copy
import json
import sys

dataPath = "./dataset/INTEGRATED-DATASET.csv"

dataSet = pd.read_csv(dataPath)
dataSet.columns = ["Name", "Borough", "Type", "InspectionSeason", "Reason", "Critical", "Score", "Grade", "GradeSeason"]
dataSet['InspectionSeason'] = dataSet['InspectionSeason'].str.replace('-INSPECTION DATE','')
dataSet['GradeSeason'] = dataSet['GradeSeason'].str.replace('-GRADE DATE','')
min_supp = 0.2*len(dataSet)
min_conf = 0.1*len(dataSet)


def get_Lk(one_item_set, depth = 4):
    Union_Lk = []
    Union_Lk.append(one_item_set)
    k = 1
    while len(Union_Lk[-1]) != 0 and k <= depth:
        Ck = apriori_gen(Union_Lk[-1], k)
        passed = []
        for idx, c in enumerate(Ck):
            cols = []
            vals = []
            for item in c:
                cols.append(item[0])
                vals.append(item[1])
            gb = dataSet.groupby(cols)
            try:
                if len(gb.get_group(tuple(vals))) >= min_supp:
                    passed.append(Ck[idx])
            except:
                print "Combination Not existed!"
        Union_Lk.append(passed)
        k = k + 1
    return Union_Lk


def apriori_gen(Lk_minus1, k):
    Ck = []
    print(len(Lk_minus1))
    for i in xrange(0, len(Lk_minus1)):
        for j in xrange(i + 1, len(Lk_minus1)):
            if check_match(Lk_minus1[i], Lk_minus1[j]):

                new_item_set = Lk_minus1[i][:]
                new_item_set.append(Lk_minus1[j][-1])
                if k == 1 or check_subset(Lk_minus1, new_item_set):
                    Ck.append(new_item_set)
                    #     sort(Ck) not sure if we need to sort it
    return Ck


def check_subset(Lk_minus1, new_item_set):
    for i in xrange(len(new_item_set)):
        subset = copy.deepcopy(new_item_set)
        del subset[i]
        if subset not in Lk_minus1:
            return False
    return True


def check_match(set1, set2):
    for i in xrange(len(set1) - 1):

        if set1[i] != set2[i]: return False
    if set1[-1][0] == set2[-1][0]:
        return False
    if set1[-1][0] != set2[-1][0] and set1[-1][1] != set2[-1][1]:
        return True


def get_L1(dataSet, one_item):
    for item in one_item:
        cntType = dataSet.groupby(item).count()
        one_item[item] = [x for x in one_item[item] if cntType.at[x, 'Name'] >= min_supp]


def init_one_item_set(one_item, one_item_set):
    for key in one_item:
        for val in one_item[key]:
            new_item_set = []
            new_item_set.append((key, val))
            one_item_set.append(new_item_set)

def get_initial(dataSet, header):
    one_item = {}
    for value in header:
        temp = dataSet[value].unique()
        one_item[value] = temp
    return one_item

header = ["Borough", "Type", "InspectionSeason", "Reason", "Critical", "Score", "Grade", "GradeSeason"]
one_item = get_initial(dataSet, header)

get_L1(dataSet, one_item)

one_item_set = []
init_one_item_set(one_item, one_item_set)


one_item_set = sorted(one_item_set, key=lambda x: (x[0], x[0][1]))
Union_Lk = get_Lk(one_item_set)

def pick_up_cal(df, result):
    temp = df
    for index in range(len(result)):
        temp = temp[temp[result[index][0]] == result[index][1]]
    return temp.shape[0]


def pick_up_num(df, num, selected, remains, index):
    result = []
    if num > len(remains) - index:
        return []
    if num == 0:
        A = pick_up_cal(df, selected + remains)
        B = pick_up_cal(df, selected)
        if B == 0: return []
        return [json.dumps({"RHS": remains, "LHS": selected, "Confidence": A * 1.0 / B})]
    result += pick_up_num(df, num, selected, remains, index + 1)
    result += pick_up_num(df, num - 1, selected + [remains[index]], remains[:index] + remains[index + 1:], index)
    return result


def generate_fit(df, result, threshold):
    submit = []
    for level, value in enumerate(result):
        # under 1st Level
        if level == 0: continue
        for index, item in enumerate(value):
            # e.g item = [('Borough', 'BRONX'), ('Grades', 'A')]
            num = level + 1
            for i in range(1, num):
                submit += pick_up_num(df, i, [], item, 0)
    return submit

def print_supply(dataSet, union):
    total = dataSet.shape[0]
    for value in union:
        for item in value:
            num = pick_up_cal(dataSet, item)
            print str(item) + ", " + str(100.0 * num/total)+"%"

print_supply(dataSet, Union_Lk)
final = generate_fit(dataSet, Union_Lk, 0.5)

confidence = 0.7

for item in final:
    temp = json.loads(item)
    if temp["Confidence"] > confidence: print temp