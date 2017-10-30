# UserModels
LSTM model for selection procedure in pupil dilation speller

TODO:

- Cross-validate the models (20 times 10-fold cross-validation)
  ~ number_median_samples_per_round(10, 5, 3, 2, 1) #{Number of rounds = 10} (olaf)
  ~ for optimal model -> add gradient feature (lennart)
  ~ for optimal model -> try model that uses only collection phase (denny)
  ~ number_of_rounds(10, 9, 8, 7, 6, 5, 4, 3, 2, 1) #{number_median_samples_per_round depends on optimal_model} (denny 1-5, lennart 6-10)
  
- Cross-validate using both incorrect and correct data
  ~ for optimal model -> train model on data initial participant and 2 additional participants
  ~ for optimal model -> train model on data from all participants
  
 
 
 
