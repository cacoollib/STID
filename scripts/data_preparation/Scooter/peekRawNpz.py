import numpy as np

# DATASET_NAME = "PEMS04"
DATASET_NAME = "Scooter"
DATA_FILE_PATH = "datasets/raw_data/{0}/{0}.npz".format(DATASET_NAME)
TARGET_CHANNEL = [0]

# read data
data = np.load(DATA_FILE_PATH)["data"]
# data = np.load(DATA_FILE_PATH)["result"]
# data = data[..., TARGET_CHANNEL]
print("raw time series shape: {0}".format(data.shape))

print('print(data[0:2, 0:3, :])')

print(data[0:2, 0:3, :])

print("raw time series shape: {0}".format(data.shape))
