import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the data from the NPZ files
data = np.load('checkpoints/tensorCsv/scooter_real_value.npy')

real_values = data

data = np.load('checkpoints/tensorCsv/prediction_error.npy')
prediction_errors = data

# Define the bin edges
bin_edges = [i for i in range(40)]  # Bins [0, 1), [1, 2), [2, 3), ...

# Calculate absolute errors
absolute_errors = np.abs(prediction_errors)

# Categorize real values into bins
real_value_bins = pd.cut(real_values.flatten(), bins=bin_edges, right=False)

# Create a DataFrame to facilitate plotting
df = pd.DataFrame({'Real Values': real_values.flatten(), 'Absolute Errors': absolute_errors.flatten()})
df['Real Value Bins'] = real_value_bins

# Create a box plot using Matplotlib
plt.figure(figsize=(10, 6))
plt.boxplot([df[df['Real Value Bins'] == real_bin]['Absolute Errors'] for real_bin in real_value_bins.categories], labels=real_value_bins.categories, showfliers=False)
plt.title('Box Plot of Absolute Error vs. Real Values')
plt.xlabel('Real Value Bins')
plt.ylabel('Absolute Errors')
plt.xticks(rotation=45)
plt.show()


