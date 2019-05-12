from keras import layers
import numpy as np
from loadingData import *
from keras import models
from keras.layers import Dense
from sklearn.preprocessing import OneHotEncoder, StandardScaler

#need to one-hot encode the Y labels
enc = OneHotEncoder()
Y = enc.fit_transform(conditions_threeway[:, np.newaxis]).toarray()
labels_train = Y[1:250]
labels_val = Y[250:]

model = models.Sequential()
model.add(Dense(16, input_dim=39912, activation='relu'))
model.add(Dense(3, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(FHC_train, labels_train, batch_size=5, epochs=50, verbose=1)
score = model.evaluate(FHC_val, labels_val)

print('Test loss:', score[0])
print('Test accuracy:', score[1])