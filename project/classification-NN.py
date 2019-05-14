from keras import layers
import numpy as np
from loadingData import *
from keras import models
from keras.layers import Dense
from sklearn.preprocessing import OneHotEncoder, StandardScaler


#three-way classification with NN
X_train = X_all[:800]
X_val = X_all[800:]
# print("Length of training data: ", len(FHC_train))
# print("Lenth of validation data: ", len(FHC_val))

#need to one-hot encode the Y labels
enc = OneHotEncoder()
#cited from https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
Y = enc.fit_transform(Y_all[:, np.newaxis]).toarray()
Y_train = Y[:800]
Y_val = Y[800:]


# # experimental attempt to transform the 2D voxel*time array
# reshaped_X = np.empty(shape = (324, 798))
# reshaped_dimension = np.empty(shape = (1, 798))
# subject = []
# dim = []
# for i in range(0, 324):
#     old_dim = FHC[i]
#     #cited from https://stackoverflow.com/questions/15956309/averaging-over-every-n-elements-of-a-numpy-array
#     new_dim = np.mean(old_dim[:(len(old_dim)// 50) * 50].reshape(-1, 50), axis=1)
#     subject.append(new_dim)
#
# reshaped_X = np.array(subject)
# print("Reshaped subject 1 X:", reshaped_X.shape)
# print("Content:", reshaped_X)
#
# reshaped_Xtrain = reshaped_X[:250]
# reshaped_Xval = reshaped_X[250:]
#
# labels_train = conditions_threeway[:250]
# labels_val = conditions_threeway[250:]

# #after averaging every 50 elements in vector, fitting a DNN on the smaller-sized input:
# smaller_model = models.Sequential()
# # smaller_model.add(Dense(32, input_dim = 798, activation='relu'))
# smaller_model.add(Dense(16, input_dim = 798, activation='relu'))
# smaller_model.add(Dense(3, activation ='softmax'))
# smaller_model.summary()
#
# smaller_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# smaller_model.fit(reshaped_Xtrain, labels_train, batch_size=324, epochs=5, verbose=1)
# score = smaller_model.evaluate(reshaped_Xval, labels_val)
#
# print('Model with reduced input: ')
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])


#another DNN on all 4 subjects (1294 trials)
model = models.Sequential()
model.add(Dense(32, input_dim = 39912, activation='relu'))
model.add(Dense(16, input_dim = 32, activation='relu'))
model.add(Dense(3, activation='softmax'))
model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=324, epochs=10, verbose=1)
score = model.evaluate(X_val, Y_val)

print('Model with all four subjects data:')
print('Train loss:', score[0])
print('Train accuracy:', score[1])
