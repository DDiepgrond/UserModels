# from LSTM import
import glob
import numpy as np
import random
import sys

"""
Structure should be:

*Most of the preprocessing is done outside of Pyhton now by Olaf, should we keep it like this?
*We now only use the data from 1 phase (choosing between A and B) and not of the other parts of Mathot's experiment

- Loading data (incl merging all 0 and 1 data)
- Creating target data
- Combining the merged 0 and 1 data with the right target data
- How many features do we want to use? (pupil dilation, derivatives etc)
- What should the sample frequency be? 
- Data augmentation
- Combining all these small functions in one final function that can be called by the experiments
"""
N_POINTS = 200
DATA_PATH = 'output'

def compute_gradient(data):
    data = np.gradient(data)
    return data


def format_data(data, min_round_len):
    data = [sum(i, []) for i in data]
    data = [map(float,i) for i in data]
    data = [i[:min_round_len] if len(i) > N_POINTS else i + [0] * (N_POINTS - len(i)) for i in data]
    return data


def merge_data(a, b):
    a = np.array(a)
    b = np.array(b)
    ab = np.array(a.tolist() + b.tolist())
    return ab


def create_target_data(len_0, len_1):
    y = np.array(np.zeros(len_0).tolist() + np.ones(len_1).tolist())
    return y


def preprocess_data(num_features):
    files_0 = glob.glob(DATA_PATH + '/0/*.dat')
    files_1 = glob.glob(DATA_PATH + '/1/*.dat')

    if len(files_0) != len(files_1):
        print('[WARNING]: Number of positive and negative files are not the same!')
        sys.exit()

    X = np.array([])
    Y = np.array([])

    files = [val for pair in zip(files_0, files_1) for val in pair]
    for i in xrange(0, len(files), 2):
        d_0 = np.load(files[i])
        d_1 = np.load(files[i + 1])

        d_0 = format_data(d_0, N_POINTS)
        d_1 = format_data(d_1, N_POINTS)

        if (num_features == 2):
            d_0_gradient = compute_gradient(d_0)
            d_1_gradient = compute_gradient(d_1)

        X = merge_data(X, merge_data(d_0, d_1))
        Y = merge_data(Y, create_target_data(len(d_0), len(d_1)))

    return (X, Y)
