# -*- coding: utf-8 -*-
import pandas as pd
import tables
from pandas.io.pickle import read_pickle


if __name__ == "__main__":

    # concat results from all classifiers
    result_dict = read_pickle("data/result.pickle")

    df = pd.DataFrame()

    for k, v in result_dict.iteritems():
        df = df.append(v[["subj", "seg", "result"]])

    df = df.set_index(["subj", "seg"])

    # output results in order of index
    print "clip,seizure,early"
    h5 = tables.open_file("data/test.h5", "r")

    for row in h5.get_node("/index").read():
        cat, subj, seg = row[0], row[1], int(row[2])
        p = df.ix[subj].ix[seg]["result"]
        print "{0}_test_segment_{1}.mat,{2},{2}".format(subj, int(seg), p)

    h5.close()


