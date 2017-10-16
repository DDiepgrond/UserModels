import sys
import glob
import random
import numpy as np
from preprocessing import *
from numpy import array
from numpy import zeros, newaxis
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from keras.preprocessing import sequence

""""
Structure: 
Basically just model compilation. This way we can create models in the experiment scripts. 

TODO
- Tune model parameters (layers of LSTM)
- Make different models so we can test them along each other

"""

N_FEATURES = 2
INPUT_SIZE = 500
HIDDEN_UNITS = 128
EPOCHS = 3
BATCH_SIZE = 5

def compile_model():
    model = Sequential()
    model.add(LSTM(HIDDEN_UNITS, input_shape=(INPUT_SIZE, N_FEATURES), return_sequences=True, activation='sigmoid'))
    model.add(Dropout(0.2))    
    model.add(LSTM(HIDDEN_UNITS))
    model.add(Dropout(0.2))
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
    return x.reshape((len(x), len(x[0]), N_FEATURES))


if __name__ == "__main__":
    model = compile_model()

    x_train, y_train = preprocess_data(N_FEATURES, INPUT_SIZE)

    x_train, y_train = shuffle_train_data(x_train, y_train)
    print(x_train.shape)
    x_train = reshape_data(x_train)

    model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE)

    scores = model.evaluate(X_test, Y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1] * 100))