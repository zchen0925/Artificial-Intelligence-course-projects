from keras import layers, models
from nilearn.image import crop_img, index_img, iter_img, load_img, concat_imgs
from nilearn.plotting import plot_stat_map, show
from loadingData import *
from sklearn.preprocessing import OneHotEncoder
import numpy as np

def loadFilteredImages(sub):
    behavioral = pd.read_csv(haxby_dataset.session_target[sub], sep=" ")
    conditions = behavioral['labels']
    print("length of all trials: ", len(conditions))
    threeway_mask = conditions.isin(['face', 'house', 'cat'])
    images = index_img(loadSubject(sub), threeway_mask)
    return images

#for subject 1, returned images are a set of 324 frames/trials, each containing 40 slices of 64*64 images
#original shape: (40, 64, 64, 324)
subj1_images = loadFilteredImages(0)
images = np.empty((40, 64, 64))
#use np.stack to reshape the 4D image array to (324, 40, 64, 64)
images = np.stack([img.dataobj for i, img in enumerate(iter_img(subj1_images))])
train_images = images[:250]
val_images = images[250:]
print("Shape of input: ", train_images.shape)
print("Content of input: ", train_images)

#need to one-hot encode the Y labels
enc = OneHotEncoder()
#cited from https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
Y = enc.fit_transform(conditions_threeway[:, np.newaxis]).toarray()
Y_train = Y[:250]
Y_val = Y[250:]

#cited from https://github.com/fchollet/deep-learning-with-python-notebooks/blob/master/5.1-introduction-to-convnets.ipynb
model = models.Sequential()
model.add(layers.Conv2D(32, kernel_size = (3, 3), activation='relu', input_shape=(40, 64, 64)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(3, activation='softmax'))
model.summary()

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images, Y_train, epochs=5, batch_size=20)

test_loss, test_acc = model.evaluate(val_images, Y_val)

print("Test loss: ", test_loss)
print("Test accuracy: ", test_acc)

#accuracy: 0.365. This is only slightly better than chance..
