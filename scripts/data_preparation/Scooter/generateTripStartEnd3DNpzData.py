# coding: utf8
import numpy as np
import csv
import pickle

# Read the CSV file and organize data

file_path = "datasets/raw_data/Scooter/griddeltasnapshots.csv"
# pickle_file_path = "datasets/raw_data/Scooter/NOT_IMPLEMENTED.pkl"
output_npz_file_path = "datasets/raw_data/Scooter/Scooter.npz"

GRID_WIDTH = 10
GRID_HEIGHT = 10

data = {}
with open(file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    # print(reader)
    for row in reader:
        # print(row)
        time = int(row['Time'])
        grid_id = GRID_WIDTH * int(row['grid_location_y']) + int(row['grid_location_x'])
        if time not in data:
            data[time] = {}
        data[time][grid_id] = [int(row['delta_trip_start_count']), int(row['delta_trip_end_count'])]

# Rearrange the data for 3-dimensional array
time_list = sorted(data.keys())
location_list = sorted(set(location for time_data in data.values() for location in time_data))
result = np.zeros((len(time_list), len(location_list), 2), dtype=int)
for i, time in enumerate(time_list):
    for j, grid_id in enumerate(location_list):
        if grid_id in data[time]:
            result[i, j] = data[time][grid_id]

# # Save the numpy array as a pickle file
# with open('result.pkl', 'wb') as pklfile:
#     pickle.dump(result, pklfile)

# Save the numpy array as npz file
np.savez(output_npz_file_path, data=result)

# Print the result (optional)
# print(result)
