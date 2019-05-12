from keras import layers
import numpy as np
from loadingData import *
from keras import models
from keras.layers import Dense
from sklearn.preprocessing import OneHotEncoder, StandardScaler

#need to one-hot encode the Y labels
enc = OneHotEncoder()
#cited from https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
Y = enc.fit_transform(conditions_threeway[:, np.newaxis]).toarray()
labels_train = Y[:250]
labels_val = Y[250:]


# experimental attempt to transform the 2D voxel*time array
reshaped_X = np.empty(shape = (324, 798))
reshaped_dimension = np.empty(shape = (1, 798))
subject = []
dim = []
# for dimension in range(0, 324):
#     for x in range(0, 797):
#         sum_series = 0
#         for i in range(0, 49):
#             index = x * 50 + i
#             sum_series += FHC[dimension][index]
#         dim.append(sum_series/49)
#     subject.append(dim)
#
# reshaped_X = np.array(subject)

for i in range(0, 324):
    old_dim = FHC[i]
    new_dim = np.mean(old_dim[:(len(old_dim)// 50) * 50].reshape(-1, 50), axis=1)
    subject.append(new_dim)

reshaped_X = np.array(subject)
print(reshaped_X.shape)
print(reshaped_X)

reshaped_Xtrain = reshaped_X[:250]
reshaped_Xval = reshaped_X[250:]

# model = models.Sequential()
# # model.add(Dense(64, input_dim = 39912, activation='relu'))
# # model.add(Dense(32, input_dim = 64, activation='relu'))
# model.add(Dense(16, input_dim = 39912, activation='relu'))
# # model.add(Dense(8, input_dim=16, activation='relu'))
# model.add(Dense(3, activation='softmax'))
# model.summary()
#
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(FHC_train, labels_train, batch_size=5, epochs=50, verbose=1)
# score = model.evaluate(FHC_val, labels_val)
#
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])

smaller_model = models.Sequential()
# smaller_model.add(Dense(64, input_dim = 798, activation='relu'))
# smaller_model.add(Dense(32, input_dim = 64, activation='relu'))
smaller_model.add(Dense(16, input_dim = 798, activation='relu'))
smaller_model.add(Dense(8, input_dim=16, activation='relu'))
smaller_model.add(Dense(3, activation='softmax'))
smaller_model.summary()

smaller_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
smaller_model.fit(reshaped_Xtrain, labels_train, batch_size=20, epochs=50, verbose=1)
score = smaller_model.evaluate(reshaped_Xval, labels_val)

print('Model with reduced input: ')
print('Test loss:', score[0])
print('Test accuracy:', score[1])