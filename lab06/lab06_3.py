'''
Lab06 for CS 344 Fall 2019
Ziqi Chen
Mar 9th 2019
'''

import numpy as np
from keras.datasets import boston_housing

(train_images, train_labels), (test_images, test_labels) = boston_housing.load_data()

def print_structures():
    print(
        #exercise 3.i
        f'Number of examples: \
            \n\tTraining set count: {len(train_images)} \
            \n\tTesting set count: {len(test_images)} \n\n',

        #exercise 3.ii
        f'Rank, shape, data type \
            \n\tTraining dimensions: {train_images.ndim} \
            \n\tTraining shape: {train_images.shape} \
            \n\tTraining data type: {train_images.dtype}\
            \n\n\tTesting dimensions: {test_images.ndim} \
            \n\tTesting shape: {test_images.shape} \
            \n\tTesting data type: {test_images.dtype} \n',
    )
print_structures()
