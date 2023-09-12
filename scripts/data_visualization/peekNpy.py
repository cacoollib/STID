import numpy as np


# read data
data = np.load('checkpoints/tensorCsv/scooter_real_value.npy')
# data = np.load(DATA_FILE_PATH)["result"]
# data = data[..., TARGET_CHANNEL]

print(data.shape)

print(data)


