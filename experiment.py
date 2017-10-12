from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import StratifiedKFold
import numpy

from LSTM import compile_model
from preprocessing import preprocess_data

""" 
Script for running different experiments using preprocessing.py which loads and preprocesses the data and 
LSTM.py that trains the model:
"""

features = 1
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# import dataset using preprocessing.py
[inputdata, targetdata] = preprocess_data(features)

# define 10-fold cross validation test harness
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
cvscores = []
for train, test in kfold.split(inputdata, targetdata):
    # Create model
    model = compile_model()
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(inputdata[train], targetdata[train], validation_split=0.2, epochs=150, batch_size=10, verbose=1)
    # evaluate the model
    scores = model.evaluate(inputdata[test], targetdata[test], verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    cvscores.append(scores[1] * 100)
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))