# -*- coding: utf-8 -*-
from seizure_detection import path
from pandas.io.pickle import read_pickle, to_pickle
from sklearn.ensemble import RandomForestClassifier


def prepare_cv_sets():
    df = read_pickle(path + "/../train_shuffled.pickle")

    # delete subject related fields
    del df["seg"]
    del df["subject"]

    # CV 80%/20%
    pivot = int(len(df.index) * 0.8)
    train_X, test_X = df.ix[:pivot], df.ix[pivot:]

    # divide into data set and target
    train_y = train_X["ictal"]
    del train_X["ictal"]

    test_y = test_X["ictal"]
    del test_X["ictal"]

    return train_X, train_y, test_X, test_y


def prepare_combat_sets():
    train_X = read_pickle(path + "/../train_shuffled.pickle")
    test_X = read_pickle(path + "/../test_shuffled.pickle")

    # delete subject related fields
    del train_X["seg"]
    del train_X["subject"]
    del test_X["seg"]
    del test_X["subject"]

    # divide into data set and target
    train_y = train_X["ictal"]
    del train_X["ictal"]

    test_y = test_X["ictal"]
    del test_X["ictal"]

    return train_X, train_y, test_X, test_y


def dirty_job(train_X, train_y, test_X):
    # create classifier
    rf = RandomForestClassifier(n_estimators=100, n_jobs=1)

    # train
    print "Training..."
    rf.fit(train_X, train_y)
    print "Ready!"

    # predict
    print "Predicting"
    z = rf.predict(test_X)
    print "Ready!"

    # save
    to_pickle(z, path + "/../result_vector.pickle")

    return z

def go():
    train_X, train_y, test_X, test_y = prepare_combat_sets()

    #z = read_pickle("../cv_result_vector.pickle")
    z = dirty_job(train_X, train_y, test_X)

    n_correct = sum(c[0] == c[1] for c in zip(z, test_y))
    n_total = len(z)

    print n_correct, n_total
    print n_correct*100.0/n_total


if __name__ == "__main__":
    go()



