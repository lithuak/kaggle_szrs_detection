# -*- coding: utf-8 -*-
import os
import pandas as pd
from pandas.io.pickle import to_pickle
from seizure_detection import path, get_subject_limits


def make_initial_dataframe(cats):
    rows = []
    for subj in os.listdir(path):
        print subj
        lims = get_subject_limits(subj)
        for cat in cats:
            for i in range(0, lims[cat]):
                rows.append({"subject": subj,
                             "seg": i+1,
                             "ictal": cat == "ictal"})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df_train = make_initial_dataframe(("ictal", "interictal"))
    to_pickle(df_train, path + "/../train_inititial.pickle")

    df_test = make_initial_dataframe(("test",))
    to_pickle(df_test, path + "/../test_inititial.pickle")

