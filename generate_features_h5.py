# -*- coding: utf-8 -*-
import tables
import numpy as np
import numpy.fft as fft
import pandas as pd
from pandas.io.pickle import read_pickle, to_pickle

def genfeu_for_sample(data):
    nchan, nsample = data.shape
    fvs = {
        "min": np.amin(data, 1),
        "max": np.amax(data, 1),
        "sum": np.sum(data, 1) * 1000000000000000 / nsample,
        "mean": np.mean(data, 1) * 1000000000000000,
        "var": np.var(data, 1),
        "std": np.std(data, 1),
        "median": np.median(data, 1),
    }
    features = {"{}_{}".format(k, i): vi for k, v in fvs.iteritems() for i, vi in enumerate(v)}

    spectrum = fft.fft(data, 8).flatten()
    features.update({"freq_{}".format(i): z.real for i, z in enumerate(spectrum)})

    return nchan, features



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
        row.update(features)

        #
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



if __name__ == "__main__":
    genfeu_for_file("train")

