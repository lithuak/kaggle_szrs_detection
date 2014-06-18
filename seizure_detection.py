# -*- coding: utf-8 -*-
import os
import re
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

# 1. Data set in non-regular:
#   a. "ictal" segments are 1sec parts of one long record
#   b. "interictal" are random independent 1sec records

path = '/media/soul/Data/kaggle/seizure_detection/clips'


def get_segment_path(subject, seg, cat="interictal"):
    return path + "/{0}/{0}_{2}_segment_{1}.mat".format(subject, seg, cat)


def get_subject_limits(subject):
    """ Given a subject gets the number of ictal, interictal and test segments """
    def get_segment_num(s):
        return int(re.split("[_.]", s)[4])
    filenames = os.listdir(path + "/" + subject)
    return {cat: max(get_segment_num(f) for f in filenames if "_" + cat + "_" in f)
            for cat in ("ictal", "interictal", "test")}


def load_segment(subject, seg, cat):
    return scipy.io.loadmat(get_segment_path(subject, seg, cat))


def paste_segments(subject, cat):
    lims = get_subject_limits(subject)

    print lims

    series = None
    for seg in range(1, lims[cat]):
        print seg
        mat = load_segment(subject, cat, seg)
        if series is None:
            series = mat["data"]
        else:
            series = np.hstack((series, mat["data"]))

    return series


def plot_data(all_data):
    for i in range(0, 16):
        data = all_data[i]
        plt.ylim([-800, 800])
        plt.plot(range(0, len(data)), data)


def plot_subject(subject):
    dpi = 96
    fig = plt.figure(figsize=(2048/dpi, 1024/dpi), dpi=dpi)

    ictal_data = paste_segments(subject, "ictal")
    inter_data = paste_segments(subject, "interictal")

    fig.add_subplot(311)
    plot_data(ictal_data)
    plot_data(inter_data)

    fig.add_subplot(312)
    plot_data(ictal_data)

    fig.add_subplot(313)
    plot_data(inter_data)

    plt.savefig(path+"/../" + subject + ".png")
    # plt.show()

if __name__ == "__main__":
    for subj in os.listdir(path):
        print get_subject_limits(subj)
        # plot_subject(subj)

# plot_subject("Dog_1")



# for i in range(0, 2):
#     data = series[i]
#     plt.ylim([-800, 800])
    # plt.plot(range(0, len(data)), data)


