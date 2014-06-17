# -*- coding: utf-8 -*-
import tables
import numpy as np
import numpy.fft as fft
import pandas as pd
from pandas.io.pickle import read_pickle, to_pickle


#
# Optimize:
#
# ? multindex
# ? map-reduce
# ? pytables for features instead of pandas?
#




def genfeu_for_sample(data):
    nchan, nsample = data.shape
    return pd.DataFrame({
                "min": np.amin(data, 1),
                "max": np.amax(data, 1),
                "sum_norm": np.sum(data, 1) * 1000000000000000 / nsample,
                "mean": np.mean(data, 1) * 1000000000000000,
                "var": np.var(data, 1),
                "std": np.std(data, 1),
                "medium": np.median(data, 1),
                "channel": np.arange(nchan)
           })


def genfeu_for_dataset(store):

    r = pd.DataFrame()

    for row in store.get_node("/index").read():
        cat, subj, seg = row[0], row[1], int(row[2])
        print cat, subj, seg

        # get data
        data = store.get_node("/{}/{}/s_{}".format(cat, subj, seg)).read()

        # calculate features
        features = genfeu_for_sample(data)
        features["subj"] = subj
        features["seg"] = seg
        features["szr"] = 1.0 if cat == "ictal" else 0.0
        features["freq"] = data.shape[1]

        r = r.append(features, ignore_index=True)

    return r


def genfeu_for_file(file):
    print "Reading " + file + " set in memory, please wait :)"
    h5 = tables.open_file("data/" + file + ".h5", "r", driver="H5FD_CORE")
    # h5 = tables.open_file("data/" + file + ".h5", "r")
    print "Done"
    print "Traversing"
    df = genfeu_for_dataset(h5)
    h5.close()
    to_pickle(df, "data/features_" + file + ".pickle")


if __name__ == "__main__":
    # genfeu_for_file("train")
    genfeu_for_file("test")

# TODO:
#
# 1) Try to normalize over min and max in whole dataset?...
#
"""
 + histogram
 + ffc
 + more data
 + other models
 + see what we can get from channel name (position?..)
 + ...and then frequency forensics is go
"""
