import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the data from the NPZ files

data = np.load('checkpoints/tensorCsv/prediction_error.npy')
prediction_errors = data

absolute_errors = np.abs(prediction_errors)

mean_absolute_error = np.mean(absolute_errors)

print("Unnormalized MAE on last test batch: " + str(mean_absolute_error))



