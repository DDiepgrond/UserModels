import sys
import glob
import random
import numpy as np
from preprocess_data import *
from numpy import array
from numpy import zeros, newaxis
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing import sequence

""""
TODO:

- Validation & testing
- Data augmentation (create more data to train on)
- Tune preprocessing parameters (i.e. sample frequency)
- Add data from other phases to the data sets
- Feature selection (derivatives?)
- Tune model parameters (layers of LSTM)
- 

"""

# Global parameters

def compile_model():
    model = Sequential()
    model.add(LSTM(32, input_shape=(250, 1), activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def shuffle_train_data(x, y):
    shuf_indices = np.arange(len(x))
    np.random.shuffle(shuf_indices)
    x = x[shuf_indices]
    y = y[shuf_indices]
    return x, y


def reshape_data(x):
    return x.reshape((len(x), len(x[0]), 1))


if __name__ == "__main__":
    model = compile_model()

    num_features = 2
    x_train, y_train = preprocess_data(num_features)

    x_train, y_train = shuffle_train_data(x_train, y_train)
    x_train = reshape_data(x_train)

    model.fit(x_train, y_train, epochs=3, batch_size=5)

    scores = model.evaluate(X_test, Y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1] * 100))