# -*- coding: utf-8 -*-
import os
import tables as tb
import numpy as np
from seizure_detection import path, get_subject_limits, load_segment

print os.getcwd()


def convert(store, cats):

    for cat in cats:
        store.createGroup("/", cat)

    atom = tb.Atom.from_dtype(np.dtype(np.float64))
    filters = tb.Filters(complib='blosc', complevel=6)

    index = []

    for cat in cats:
        for subj in os.listdir(path):
            print subj
            lims = get_subject_limits(subj)
            grp = store.createGroup("/" + cat, subj)
            for i in range(1, lims[cat] + 1):
                index.append((cat, subj, i))
                data = load_segment(subj, i, cat)["data"]
                ca = store.create_carray(grp, "s_{}".format(i), atom, data.shape, filters=filters)
                ca[:] = data

    pindex = store.createArray("/", "index", index)
    pindex[:] = index

    store.flush()
    store.close()


def convert_all():
    train_file = tb.openFile("./data/train.h5", mode="w", title="Test file")
    convert(train_file, ["ictal", "interictal"])
    test_file = tb.openFile("./data/test.h5", mode="w", title="Test file")
    convert(test_file, ["test"])


# def process_sample(sample_id, set_cat, subject, cat, segment, channel, data):
#     pass
#
#     return sample_id, {"a" + channel: 12,
#                        "b" + channel: 13}


if __name__ == "__main__":
    convert_all()



