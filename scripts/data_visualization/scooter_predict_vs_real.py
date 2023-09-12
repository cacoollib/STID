import numpy as np
import matplotlib.pyplot as plt

# Load the data from the NPZ files
real_values = np.load('checkpoints/tensorCsv/scooter_real_value.npy')
predicted_values = np.load('checkpoints/tensorCsv/scooter_prediction.npy')

# Flatten the arrays to make them 1D
real_values = real_values.flatten()
predicted_values = predicted_values.flatten()

# Create a dictionary to count occurrences of (real, predicted) pairs
occurrence_count = {}
for real, predicted in zip(real_values, predicted_values):
    pair = (real, predicted)
    occurrence_count[pair] = occurrence_count.get(pair, 0) + 1

# Extract unique (real, predicted) pairs and their counts
unique_pairs = list(occurrence_count.keys())
counts = [occurrence_count[pair] for pair in unique_pairs]

# Unzip the unique pairs to separate real and predicted values
real_values, predicted_values = zip(*unique_pairs)

# Create the bubble plot
plt.figure(figsize=(10, 8))
plt.scatter(real_values, predicted_values, s=counts, alpha=0.5)
plt.xlabel('Truth Values')
plt.ylabel('Predicted Values')
plt.title('Bubble Plot of Truth vs. Predicted Values')
plt.grid(True)

# Show the plot
plt.show()
