#!/usr/bin/python
# Filename: main.py
"""
Created on Thu May 30 00:23:55 2019

@author: Anshay
Main file for cats vs dogs classification

Runs cats vs dogs classification on selected dataset.
Loads data, visualizes data, fetch/train model, saves
model and evaluates the model.
"""

## import modules
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import model_gen
import input_image

## define metadata
print("\nDefining metadata")
metadata = {'Nrows':150, 'Ncols':150, 'BATCH_SIZE':100, 'NUM_EPOCHS':10,
            'FILTER_SIZE':(3,3)}
print("\nMetadata defined")

## load data - change directories to the location of data
print("\nLoading data...")
train_dir = "D:\\Datasets\\cats_vs_dogs\\train\\"
val_dir = "D:\\Datasets\\cats_vs_dogs\\val\\"
test_dir = "D:\\Datasets\\cats_vs_dogs\\test\\"

train_data_gen = ImageDataGenerator(rescale=1./255,
                              horizontal_flip=True,
                              rotation_range=40,
                              width_shift_range=0.2,
                              height_shift_range=0.2,
                              zoom_range=0.5,
                              shear_range=0.2
                              )
val_data_gen = ImageDataGenerator(rescale=1./255)

train_gen = train_data_gen.flow_from_directory(
                    train_dir,
                    target_size=((metadata['Nrows'], metadata['Ncols'])),
                    batch_size=metadata['BATCH_SIZE'],
                    class_mode='binary')

val_gen = val_data_gen.flow_from_directory(
                    val_dir,
                    target_size=((metadata['Nrows'], metadata['Ncols'])),
                    batch_size=metadata['BATCH_SIZE'],
                    class_mode='binary')

test_gen = val_data_gen.flow_from_directory(
                    test_dir,
                    target_size=((metadata['Nrows'], metadata['Ncols'])),
                    class_mode='binary')
print("\nData Generators defined")

## fetch model (training)
print("\nTraining model...")
model = model_gen.fetch_model(train_gen, val_gen, metadata)
print("\nTraining Complete")

## test model (testing)
print("\nEvaluating model on test data")
evaluations = model.evaluate_generator(test_gen)
print("\nEvaluations:")
print(evaluations)
print("\nTesting Complete")

## predict for new uploaded images
print("\nPredict on input image...")
inpImg = input_image.inpImg()
prediction = model.predict(inpImg)
if prediction > 0.5:
    print ("DOG")
else:
    print ("CAT")
