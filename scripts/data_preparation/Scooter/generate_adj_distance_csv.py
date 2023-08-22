import pandas as pd

RANDOM_SEED = 42
GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_SIDE_LENGTH = 250.0  # Each cell in the grid is 250x250m

distance_list = []

for i in range(GRID_HEIGHT):
    for j in range(GRID_WIDTH):
        # distance to right adjacent cell
        if j < GRID_WIDTH - 1:
            distance_list.append({
                "from": i * GRID_WIDTH + j,
                "to": i * GRID_WIDTH + j + 1,
                "cost": CELL_SIDE_LENGTH
            })

        # distance to lower adjacent cell
        if i < GRID_HEIGHT - 1:
            distance_list.append({
                "from": i * GRID_WIDTH + j,
                "to": (i + 1) * GRID_WIDTH + j,
                "cost": CELL_SIDE_LENGTH
            })

df = pd.DataFrame(distance_list)

# print(df)
df.to_csv('./datasets/raw_data/Scooter/Scooter.csv', index=False)