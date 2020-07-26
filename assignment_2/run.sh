#!/bin/bash

python3 MyClassifier.py pima.csv test.csv 1NN

# Note to try out the cross validation, uncomment the below
# python3 MyClassifier.py pima_cross_input.csv pima-folds.csv 1NN cross