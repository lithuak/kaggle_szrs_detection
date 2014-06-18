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
    return nchan, np.concatenate([
        # !+ this can be automated
        np.amin(data, 1),
        np.amax(data, 1),
        np.sum(data, 1) * 1000000000000000 / nsample,
        np.mean(data, 1) * 1000000000000000,
        np.var(data, 1),
        np.std(data, 1),
        np.median(data, 1),
    ])


def genfeu_for_dataset(store):
    datasets = {}

    for row in store.get_node("/index").read():
        cat, subj, seg = row[0], row[1], int(row[2])
        print cat, subj, seg

        # get data
        data = store.get_node("/{}/{}/s_{}".format(cat, subj, seg)).read()

        # calculate features
        nchan, features = genfeu_for_sample(data)

        # make row
        row = {
                "subj": subj,
                "seg": seg,
                "szr": 1.0 if cat == "ictal" else 0.0,
               }
        row.update({"f_{}".format(i): f for i, f in enumerate(features) })

        # append to corresponding dataset
        if not nchan in datasets:
            datasets[nchan] = []
        datasets[nchan].append(row)

    return {k: pd.DataFrame(v) for k, v in datasets.iteritems()}



def genfeu_for_file(file):
    print "Reading " + file + " set in memory, please wait :)"
    # h5 = tables.open_file("data/" + file + ".h5", "r", driver="H5FD_CORE")
    h5 = tables.open_file("data/" + file + ".h5", "r")
    print "Done"
    print "Traversing"
    r = genfeu_for_dataset(h5)
    h5.close()
    to_pickle(r, "data/features_" + file + ".pickle")

    # for k, v in r.iteritems():
    #     print k, v.shape



if __name__ == "__main__":
    genfeu_for_file("train")
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
