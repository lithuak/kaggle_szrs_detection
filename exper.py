# -*- coding: utf-8 -*-
from pandas.io.pickle import read_pickle, to_pickle
df = read_pickle("data/features_train.pickle")

# df[64].set_index(["subj", "seg"])
# t = range(0, 2745)
# df[64]["t"] = t
# print df[64][]


