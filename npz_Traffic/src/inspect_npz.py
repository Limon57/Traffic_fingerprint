import numpy as np

data = np.load("data/Front.npz")

labels = data["y"]

print("Unique labels:")
print(np.unique(labels))

print("Number of websites:")
print(len(np.unique(labels)))