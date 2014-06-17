# -*- coding: utf-8 -*-
import os
import re
import numpy as np
import pandas as pd
from pandas.io.pickle import read_pickle, to_pickle
from seizure_detection import path, get_segment_path, load_segment



# + pandas df.sum, mean, etc. (see table and use them all), to calc stats

# 0. save dataset
# 1. get row from df
# 2. detect file by row, read it
# 3. calculate features
# 4. CV
# 5. classifier
# 6. train, submit

# fns = ("min", "max", "sum", "mean", "median", "mad", "var", "std")
fns = ("min", "max", "sum", "mean", "var", "std")


def init_dataset_features(df):
    for f in fns:
        for i in range(0, 16):
            df[f+"_"+str(i)] = 0
    df["freq"] = 0
    #
    # ! since we submit latency prob the same as seizure prob now (from forum)
    #
    # df["latency"] = 0


def fill_row_features(df, i, segment):

    df.loc[i, "freq"] = segment.ix[0].size

    for f in fns:
        for j in range(0, 16):
            val = getattr(segment.ix[j], f)()
            df.loc[i, f+"_"+str(j)] = val


def fill_dataset_features(df, which="train"):
    for i, row in df.iterrows():
        if which == "train":
            cat = "ictal" if row["ictal"] else "interictal"
        else:
            cat = "test"
        data = load_segment(row["subject"], row["seg"], cat)
        print row["subject"], cat, row["seg"]

        segment = pd.DataFrame(data["data"])
        fill_row_features(df, i, segment)

    #
    # ! since we submit latency prob the same as seizure prob now (from forum)
    #
    # if row["ictal"] and "latency" in data:
    #     df.loc[i, "latency"] = int(data["latency"][0])


def shuffle_df(df):
    import random
    sh_ix = range(0, df.index.size)
    random.shuffle(sh_ix)
    return df.reindex(index=sh_ix)


def go(which):
    df = read_pickle(path + "/../" + which + "_inititial.pickle")
    init_dataset_features(df)
    fill_dataset_features(df, which)
    df = shuffle_df(df)
    to_pickle(df, path + "/../" + which + "_features.pickle")



if __name__ == "__main__":
    #go("train")
    go("test")


"""
    Interesting thougts:
    0) FIX LATENCY!!!
    0.5) возможно настроить PyCharm и нормальный пайплайн в линухе
    1) outliers in interictal data
    2) check the names of sensors (electrodes) - are they different.
       If yes - include as features.
    3) предсказывать latency!!! (пока тупо в RF)
    4) посмотреть дополнительные данные на сайте
    5) исследовать зеленую полосочку
    6) RF может выдавать вероятности, а не 1/0
    7) поиграться с гиперпараметрами RF
"""

