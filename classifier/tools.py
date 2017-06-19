import numpy as np


def dataset_to_sample(dataset, column=None):
    if column:
        return np.array(list(dataset[column].values), ndmin=2)
    else:
        return np.array(list(dataset.values), ndmin=2)
