# -*- coding: utf-8 -*-
"""Assignment06.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BxeTQ4nrUn1cmmuyT-rqwslQeW07jGqW

#Muhammad Asmar (Z23470131)

Google Colab Link: https://colab.research.google.com/drive/1BxeTQ4nrUn1cmmuyT-rqwslQeW07jGqW?usp=sharing

#Problem 1
"""

import numpy as np
from keras.datasets import cifar10
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
labels = np.array(["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"])
classes = np.unique(y_train)

#randomly select 20% of the data for validation set
#shuffle training data
num_training_images = x_train.shape[0]
training_indices = np.arange(0, num_training_images)
training_indices_shuffled = np.random.permutation(training_indices)
x_train = x_train[training_indices_shuffled, :, :]
y_train = y_train[training_indices_shuffled]

#select 20% of training data for validation
x_val = x_train[0:int(.2 * num_training_images), :, :]
y_val = y_train[0:int(.2 * num_training_images)]
#the rest is training data
x_train = x_train[int(.2 * num_training_images):, :, :]
y_train = y_train[int(.2 * num_training_images):]

#scale pixel values from 0 to 1
x_train = x_train.astype("float32")
x_val = x_val.astype("float32")
x_test = x_test.astype("float32")
x_train /= 255
x_val /= 255
x_test /= 255

#convert labels to binary class matrices
y_train_c = to_categorical(y_train, len(classes))
y_val_c = to_categorical(y_val, len(classes))
y_test_c = to_categorical(y_test, len(classes))

#flatten images into one vector for fully connected network (1 x 3072)
x_train_flatten = np.reshape(x_train, (x_train.shape[0], x_train.shape[1] * x_train.shape[2] * x_train.shape[3]))
x_val_flatten = np.reshape(x_val, (x_val.shape[0], x_val.shape[1] * x_val.shape[2] * x_val.shape[3]))
x_test_flatten = np.reshape(x_test, (x_test.shape[0], x_test.shape[1] * x_test.shape[2] * x_test.shape[3]))

#define the model (3072, 4096, 1024, adam, lr = .001)
#50 epochs, batch size = 16
cifar10_fc_model = Sequential(name="cifar10_fc_model")
cifar10_fc_model.add(Dense(input_dim = x_train_flatten.shape[1], units=3072, activation="relu", name="hidden_layer_1"))
cifar10_fc_model.add(Dense(units=4096, activation="relu", name="hidden_layer_2"))
cifar10_fc_model.add(Dense(units=1024, activation="relu", name="hidden_layer_3"))
cifar10_fc_model.add(Dense(units=len(classes), activation="softmax", name="output_layer"))
cifar10_fc_model.summary()
cifar10_fc_model.compile(loss="categorical_crossentropy",
                optimizer=Adam(lr=0.001),
                metrics=["acc"])
history = cifar10_fc_model.fit(x_train_flatten, y_train_c, batch_size=16, epochs=50)

"""#Problem 2"""

import numpy as np
from keras.datasets import cifar10
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Activation, Dropout, Flatten, MaxPooling2D
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

#import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
classes = np.unique(y_train)

#randomly select 20% of the data for validation set
#shuffle training data
num_training_images = x_train.shape[0]
training_indices = np.arange(0, num_training_images)
training_indices_shuffled = np.random.permutation(training_indices)
x_train = x_train[training_indices_shuffled, :, :]
y_train = y_train[training_indices_shuffled]

#select 20% of training data for validation
x_val = x_train[0:int(.2 * num_training_images), :, :]
y_val = y_train[0:int(.2 * num_training_images)]
#the rest is training data
x_train = x_train[int(.2 * num_training_images):, :, :]
y_train = y_train[int(.2 * num_training_images):]

#scale pixel values from 0 to 1
x_train = x_train.astype("float32")
x_val = x_val.astype("float32")
x_test = x_test.astype("float32")
x_train /= 255
x_val /= 255
x_test /= 255

#convert labels to binary class matrices
y_train_c = to_categorical(y_train, len(classes))
y_val_c = to_categorical(y_val, len(classes))
y_test_c = to_categorical(y_test, len(classes))

#define model
cifar10_conv_model = Sequential(name="conv_model")
#first convolutional block
cifar10_conv_model.add(Conv2D(32, (3, 3), padding="same", input_shape=x_train.shape[1:], name="conv_layer_1"))
cifar10_conv_model.add(Activation("relu", name="activation_1"))
cifar10_conv_model.add(Conv2D(32, (3, 3), name="conv_layer_2"))
cifar10_conv_model.add(Activation("relu", name="activation_2"))
cifar10_conv_model.add(MaxPooling2D(pool_size=(2,2), name="pooling_1"))
#second convolutional block
cifar10_conv_model.add(Conv2D(64, (3, 3), padding="same", name="conv_layer_3"))
cifar10_conv_model.add(Activation("relu", name="activation_3"))
cifar10_conv_model.add(Conv2D(64, (3, 3), name="conv_layer_4"))
cifar10_conv_model.add(Activation("relu", name="activation_4"))
cifar10_conv_model.add(MaxPooling2D(pool_size=(2,2), name="pooling_2"))
#flattening layer
cifar10_conv_model.add(Flatten(name="flatten"))
#fully-connnected layer (512 nodes)
cifar10_conv_model.add(Dense(units=512, activation="relu", name="fc_layer"))
cifar10_conv_model.add(Dropout(0.5, name="dropout"))
#output layer
cifar10_conv_model.add(Dense(units=len(classes), activation="softmax", name="output_layer"))
cifar10_conv_model.summary() #display model architecture

save_path = "/content/drive/My Drive/cifar10_convolutional_model.h5"
callbacks_save = ModelCheckpoint(save_path, monitor="val_loss", verbose=0, save_best_only=True, save_freq='epoch')
cifar10_conv_model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.001),
                           metrics=["acc"])
history = cifar10_conv_model.fit(x_train, y_train_c, batch_size=16, epochs=50, verbose=1,
                                 validation_data=(x_val, y_val_c), callbacks=[callbacks_save])

from keras.models import load_model
#load the best model based on validation loss
best_model = load_model(save_path)
#evaluate model on test samples
score = best_model.evaluate(x_test, y_test_c)
print("Testing Set Loss: " + str(score[0]))
print("Testing Set Accuracy: " + str(score[1]))