#!/bin/bash
set -e
python generate_features_h5.py
python train_rf.py
python prepare_submit.py | tee data/result.csv


