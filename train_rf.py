# -*- coding: utf-8 -*-
import random
from seizure_detection import path
from pandas.io.pickle import read_pickle, to_pickle
from sklearn.ensemble import RandomForestClassifier

# TODO:
# 4) feature importance
# 1) try log_probabs
# 2) fft
# 3) more data

def prepare_cv_sets():
    df = read_pickle("data/features_train.pickle")

    # shuffle
    shff_index = range(0, df.shape[0])
    random.seed(13)
    random.shuffle(shff_index)
    df = df.reindex(index=shff_index)

    # delete subject related fields
    del df["seg"]
    del df["subj"]

    # CV 80%/20%
    pivot = int(len(df.index) * 0.8)
    train_X, test_X = df.ix[:pivot], df.ix[pivot:]

    # divide into data set and target
    train_y = train_X["szr"]
    del train_X["szr"]

    test_y = test_X["szr"]
    del test_X["szr"]

    return train_X, train_y, test_X, test_y


def dirty_job(train_X, train_y, test_X):
    # create classifier
    rf = RandomForestClassifier(n_estimators=4000, n_jobs=8,
                                verbose=10)

    # train
    print "Training..."
    rf.fit(train_X, train_y)
    print "Ready!"

    # predict
    print "Predicting"

    # TODO: ?! try predict_log
    z = rf.predict_proba(test_X)
    print "Ready!"

    return z


def go():
    train_dict = read_pickle("data/features_train.pickle")
    test_dict = read_pickle("data/features_test.pickle")

    for k in train_dict.iterkeys():
        data_columns = [col for col in train_dict[k].columns
                        if col not in set(["seg", "subj", "szr"])]

        z = dirty_job(train_dict[k][data_columns],
                      train_dict[k]["szr"],
                      test_dict[k][data_columns])

        test_dict[k]["result"] = z[:, 1]

    # save
    to_pickle(test_dict, "data/result.pickle")

    # !+ calc AUC
    # ...


if __name__ == "__main__":
    go()



