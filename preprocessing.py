# from LSTM import
import glob
import numpy as np
import random
import sys
from scipy.interpolate import interp1d

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
DATA_PATH = 'output'

def compute_gradient(data):
    data = np.gradient(data)
    return data


# Merges all selection loop arrays and maps them from string to floats. If they are too long, it cuts them on
# min_round_len (trimming) and if they are too short, it pads them with zeros (zero-padding).
def format_data(data, min_round_len):
    data = [sum(i, []) for i in data]
    data = [map(float,i) for i in data]
    data = [i[:min_round_len] if len(i) > min_round_len else i + [0] * (min_round_len - len(i)) for i in data]
    # Linearly interpolate the data to get rid of the zeros (mainly for blinks and other noise).
    for sl in data:
        idx_array = np.arange(len(sl))
        idx = np.nonzero(sl)[0]
        interp = interp1d(idx_array[idx], sl[idx])
        data[sl] = interp(idx_array)
    return data


def merge_data(a, b):
    a = np.array(a)
    b = np.array(b)
    ab = np.array(a.tolist() + b.tolist())
    return ab


def create_target_data(len_0, len_1):
    y = np.array(np.zeros(len_0).tolist() + np.ones(len_1).tolist())
    return y

def preprocess_data(num_features, n_points):
    files_0 = glob.glob(DATA_PATH + '/0/*.dat')
    files_1 = glob.glob(DATA_PATH + '/1/*.dat')

    if len(files_0) != len(files_1):
        print('[WARNING]: Number of positive and negative files are not the same!')
        sys.exit()

    X = np.array([])
    Y = np.array([])

    plot_d0 = []
    plot_y = []
    dg_0 = []

    files = [val for pair in zip(files_0, files_1) for val in pair]
    for i in xrange(0, len(files), 2):
        d_0 = np.load(files[i])
        d_1 = np.load(files[i + 1])

        print(d_0)
        
        d_0 = format_data(d_0, n_points)
        d_1 = format_data(d_1, n_points)
        
        l = len(d_0) if len(d_0) < len(d_1) else len(d_1)
        for i in xrange(l):
            plot_d0 = merge_data(plot_d0, d_0[i])
            plot_d0 = merge_data(plot_d0, [0] * 5)
            plot_y = merge_data(plot_y, [0] * len(d_0[i]) + [0] * 5)
            plot_d0 = merge_data(plot_d0, d_1[i])
            plot_d0 = merge_data(plot_d0, [0] * 5)
            plot_y = merge_data(plot_y, [1] * len(d_1[i]) + [0] * 5)
            dg_0 = merge_data(dg_0, compute_gradient(d_0[i]))
            dg_0 = merge_data(dg_0, [0] * 5)
            dg_0 = merge_data(dg_0, compute_gradient(d_1[i]))
            dg_0 = merge_data(dg_0, [0] * 5)
        
        if (num_features >= 2):
            d_0_gradient = compute_gradient(d_0)
            d_1_gradient = compute_gradient(d_1)
            d_0 = np.stack((d_0, d_0_gradient[0]), axis=-1)
            d_1 = np.stack((d_1, d_1_gradient[0]), axis=-1)
        
        X = merge_data(X, merge_data(d_0, d_1))
        Y = merge_data(Y, create_target_data(len(d_0), len(d_1)))
    
    np.savetxt('d0.csv', plot_d0)
    np.savetxt('y.csv', plot_y)
    np.savetxt('g0.csv', dg_0)

    return (X, Y)
