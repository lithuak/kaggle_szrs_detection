# -*- coding: utf-8 -*-
import random
from seizure_detection import path
from pandas.io.pickle import read_pickle, to_pickle


# 1. take bottom 20% as validation
# 2. as for test - submit avg latency as latency (later differ by freq)


def shuffle_df(df):
    sh_ix = range(0, df.index.size)
    random.shuffle(sh_ix)
    return df.reindex(index=sh_ix)

def go(which):
    df = read_pickle(path + "/../{}_features.pickle".format(which))
    df = shuffle_df(df)
    to_pickle(df, path + "/../{}_shuffled.pickle".format(which))

if __name__ == "__main__":
    go("test")

