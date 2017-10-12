from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import StratifiedKFold
import numpy

from LSTM import compile_model
from preprocessing import preprocess_data

""" 
File with functions to perform different experiments on Mathot's data with our model(s)

Contains:
- 10-fold cross-validation 
- 
"""

features = 1
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# import dataset using preprocessing.py
[inputdata, targetdata] = preprocess_data(features)

def cross_validation(fold)
    # define 10-fold cross validation test harness
    kfold = StratifiedKFold(n_splits=fold, shuffle=True, random_state=seed)
    cvscores = []
    for train, test in kfold.split(inputdata, targetdata):
        # Create model
        model = compile_model()

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # validation split is nu nog 0.2 maar geen idee of dat valideren hoeft als je al test met cross validation
        model.fit(inputdata[train], targetdata[train], validation_split=0.2, epochs=3, batch_size=5, verbose=1)
        scores = model.evaluate(inputdata[test], targetdata[test], verbose=0)

        print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
        cvscores.append(scores[1] * 100)
    print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))

