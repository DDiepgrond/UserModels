import sys
import glob
import random
import numpy as np
from numpy import array
from numpy import zeros, newaxis
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing import sequence

N_POINTS = 200
DATA_PATH = 'output'

def format_data(data, min_round_len):
    data = [sum(i, []) for i in data]
    data = [map(float,i) for i in data]
    data = [i[:min_round_len] if len(i) > N_POINTS else i + [0] * (N_POINTS - len(i)) for i in data]
    return data

def compile_model():
    model = Sequential()
    #model.add(LSTM(100, input_shape = (1, 1), activation='sigmoid'))
    model.add(LSTM(100, input_shape = (N_POINTS, 1), activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def merge_data(a, b):
    a = np.array(a)
    b = np.array(b)
    ab = np.array(a.tolist() + b.tolist())
    return ab

def create_target_data(len_0, len_1):
    y = np.array(np.zeros(len_0).tolist() + np.ones(len_1).tolist())
    return y

def shuffle_train_data(x, y):
    shuf_indices = np.arange(len(x))
    np.random.shuffle(shuf_indices)
    x = x[shuf_indices]
    y = y[shuf_indices]
    return x, y

def reshape_data(x):
    return x.reshape((len(x), N_POINTS, 1))

if __name__ == "__main__":    
    model = compile_model()    

    files_0 = glob.glob(DATA_PATH + '/0/*.dat')
    files_1 = glob.glob(DATA_PATH + '/1/*.dat')

    if len(files_0) != len(files_1):
        print('[WARNING]: Number of positive and negative files are not the same!')
        sys.exit()
    
    x_train = np.array([])
    y_train = np.array([])

    files = [val for pair in zip(files_0, files_1) for val in pair]
    for i in xrange(0,len(files),2):
        d_0 = np.load(files[i])
        d_1 = np.load(files[i+1])

        d_0 = format_data(d_0, N_POINTS)
        d_1 = format_data(d_1, N_POINTS)

        #if (len(d_0[0]) >= N_POINTS and len(d_1[0]) >= N_POINTS):
        #np.savetxt('0.csv', d_0[0], fmt='%1.2f')
        #np.savetxt('1.csv', d_1[0], fmt='%1.2f')
        #sys.exit()
         
        x_train = merge_data(x_train, merge_data(d_0, d_1))
        y_train = merge_data(y_train, create_target_data(len(d_0), len(d_1)))
        #y_train = merge_data(y_train, create_target_data(sum([len(i) for i in d_0]), sum([len(i) for i in d_1])))
       

    x_train, y_train = shuffle_train_data(x_train, y_train)
    x_train = reshape_data(x_train)
    
    #for i in xrange(len(x_train)):
        #x = x_train[i].reshape(N_POINTS, 1, 1)
        #y = y_train[i:len(x)]
    model.fit(x_train, y_train, epochs=1, batch_size=1)
    sys.exit()
    scores = model.evaluate(X_test, Y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1]*100))