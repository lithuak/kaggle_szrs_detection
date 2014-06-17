# -*- coding: utf-8 -*-
import random
from seizure_detection import path
from pandas.io.pickle import read_pickle, to_pickle
from sklearn.ensemble import RandomForestClassifier


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


def prepare_combat_sets():
    train_X = read_pickle(path + "/../train_shuffled.pickle")
    test_X = read_pickle(path + "/../test_shuffled.pickle")

    # delete subject related fields
    del train_X["seg"]
    del train_X["subject"]
    del test_X["seg"]
    del test_X["subject"]

    # divide into data set and target
    train_y = train_X["szr"]
    del train_X["szr"]

    test_y = test_X["szr"]
    del test_X["szr"]

    return train_X, train_y, test_X, test_y


def dirty_job(train_X, train_y, test_X):
    # create classifier
    rf = RandomForestClassifier(n_estimators=200, n_jobs=8,
                                verbose=10)

    # train
    print "Training..."
    rf.fit(train_X, train_y)
    print "Ready!"

    # predict
    print "Predicting"
    z = rf.predict(test_X)
    print "Ready!"

    # save
    to_pickle(z, path + "data/z.pickle")

    return z

def go():
    # train_X, train_y, test_X, test_y = prepare_combat_sets()
    train_X, train_y, test_X, test_y = prepare_cv_sets()

    z = dirty_job(train_X, train_y, test_X)

    n_correct = sum(c[0] == c[1] for c in zip(z, test_y))
    n_total = len(z)

    print n_correct, n_total
    print n_correct*100.0/n_total


if __name__ == "__main__":
    go()

    # save z to file
    # group by and calculate real score
    # save random forest to file
    # classify for test set
    # output, submit


