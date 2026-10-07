from ase.io import iread, write
import random

input_file = "Data.extxyz"
train_file = "train.extxyz"
test_file = "test.extxyz"

train_fraction = 0.8
random.seed(42)

# First count frames
frames = list(iread(input_file))
total = len(frames)

indices = list(range(total))
random.shuffle(indices)

n_train = int(total * train_fraction)
train_indices = set(indices[:n_train])

for i, atoms in enumerate(frames):
    if i in train_indices:
        write(train_file, atoms, format="extxyz", append=True)
    else:
        write(test_file, atoms, format="extxyz", append=True)
