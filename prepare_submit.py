# -*- coding: utf-8 -*-
import os
from seizure_detection import path, get_subject_limits
from pandas.io.pickle import read_pickle, to_pickle

f = open(path + "/../result.csv", "w")

def pr(s):
    print s
    f.write(s+"\n")


if __name__ == "__main__":
    test_df = read_pickle(path + "/../test_shuffled.pickle")
    z = read_pickle(path + "/../result_vector.pickle")

    # merge test set and results
    df = test_df[["seg", "subject"]]
    df["result"] = z

    # cals expected latency
    # train_df = read_pickle(path + "/../train_shuffled.pickle")
    # print train_df[train_df["ictal"]==False]["latency"]

    pr("clip,seizure,early")

    for subj in os.listdir(path):
        lims = get_subject_limits(subj)
        for i in range(1, lims["test"]+1):
            result = df[df["seg"] == i][df["subject"] == subj]["result"].values[0]
            result_out = 1 if result else 0
            pr("{}_test_segment_{}.mat,{},{}".format(subj, i, result_out, result_out))

