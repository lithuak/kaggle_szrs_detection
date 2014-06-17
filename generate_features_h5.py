# -*- coding: utf-8 -*-
import tables


def features_channel(channel):
    pass


def features_sample(sample):
    pass



def traverse(store):

    for szr in store.walk_nodes("/", "CArray"):
        data = szr.read()

        # ? should be attributes?...
        (_, cat, subj, seg) = szr._v_pathname.split("/")
        seg = int(seg[2:])




if __name__ == "__main__":
    print "Reading train set in memory, please wait :)"
    # h5 = tables.open_file("data/train.h5", "r", driver="H5FD_CORE")
    h5 = tables.open_file("data/train.h5", "r")
    print "Done"
    print "Traversing"
    traverse(h5)

