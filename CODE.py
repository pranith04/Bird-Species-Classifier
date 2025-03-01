# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Hk-JK9SjwLDohTojmPFjoywGJWWTA8C5
"""

import kagglehub

try:
    # Download latest version of the CUB-200-2011 dataset
    path = kagglehub.dataset_download("wenewone/cub2002011")
    print("Path to dataset files:", path)
except Exception as e:
    print(f"Error downloading dataset: {e}")

import os
import kagglehub

# Download dataset
path = kagglehub.dataset_download("wenewone/cub2002011")
print("Dataset path:", path)

# List all files in the dataset directory
print("\nFiles in the dataset directory:")
for root, dirs, files in os.walk(path):
    for file in files:
        print(os.path.join(root, file))

# Print specific paths
print("\nChecking specific file paths:")
print("Full dataset path:", path)
files_in_path = os.listdir(path)
print("Files in path:", files_in_path)

import os
import shutil
import tarfile
import kagglehub

# Download dataset
path = kagglehub.dataset_download("wenewone/cub2002011")
print("Dataset path:", path)

# Function to extract .tar or .tgz files
def extract_archive(src_dir, extract_path='./'):
    for item in os.listdir(src_dir):
        full_path = os.path.join(src_dir, item)

        # Check if it's a .tar or .tgz file
        if item.endswith('.tar') or item.endswith('.tgz'):
            try:
                with tarfile.open(full_path, "r:*") as tar:
                    tar.extractall(path=extract_path)
                print(f"Extracted: {item}")
            except Exception as e:
                print(f"Error extracting {item}: {e}")

        # If it's a directory, copy its contents
        elif os.path.isdir(full_path):
            try:
                dest = os.path.join(extract_path, item)
                shutil.copytree(full_path, dest, dirs_exist_ok=True)
                print(f"Copied directory: {item}")
            except Exception as e:
                print(f"Error copying directory {item}: {e}")

# Extract files from each subdirectory
subdirs = ['CUB_200_2011', 'segmentations', 'cvpr2016_cub']
for subdir in subdirs:
    full_subdir_path = os.path.join(path, subdir)
    print(f"\nProcessing {subdir}:")
    extract_archive(full_subdir_path)

print("\nExtraction complete.")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

import os

# Path to the parent directory
parent_directory = '/root/.cache/kagglehub/datasets/wenewone/cub2002011/versions/7/CUB_200_2011/images'

# List of directories inside the parent directory
directories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]

directories = sorted(directories)
print(directories)

import os
import numpy as np
from PIL import Image

def mask_image(directories):
    os.makedirs('/content/Masked_Images', exist_ok=True)

    for directory in directories:
        img_directory = f'/root/.cache/kagglehub/datasets/wenewone/cub2002011/versions/7/CUB_200_2011/images/{directory}'
        seg_directory = f'/root/.cache/kagglehub/datasets/wenewone/cub2002011/versions/7/segmentations/{directory}'

        # List and sort files
        jpg_files = sorted([img for img in os.listdir(img_directory) if img.endswith('.jpg')])
        png_files = sorted([img for img in os.listdir(seg_directory) if img.endswith('.png')])

        # Filter mismatched files
        jpg_files_filtered = [jpg for jpg in jpg_files if jpg.replace('.jpg', '.png') in png_files]
        png_files_filtered = [png for png in png_files if png.replace('.png', '.jpg') in jpg_files]

        # Ensure both arrays have the same length
        assert len(jpg_files_filtered) == len(png_files_filtered), "Mismatch between .jpg and .png files."

        # Shuffle indexes
        indexes = np.arange(len(jpg_files_filtered))
        np.random.shuffle(indexes)

        # Split indexes
        split_point = int(0.8 * len(jpg_files_filtered))
        train_indexes = indexes[:split_point]
        test_indexes = indexes[split_point:]
        train_split_point = int(0.75 * len(train_indexes))
        train_subset = train_indexes[:train_split_point]
        validation_subset = train_indexes[train_split_point:]

        print(f"Train indexes: {train_subset}")
        print(f"Validation indexes: {validation_subset}")
        print(f"Test indexes: {test_indexes}")

        split_indexes = [train_subset, validation_subset, test_indexes]
        split_dir = ['train', 'valid', 'test']

        jpg_array = np.array(jpg_files_filtered)
        png_array = np.array(png_files_filtered)

        for i in range(3):
            masked_image_count = 0
            for jpg_file, png_file in zip(jpg_array[split_indexes[i]], png_array[split_indexes[i]]):
                # Load the original image and mask using Pillow
                image = Image.open(f'{img_directory}/{jpg_file}')
                mask = Image.open(f'{seg_directory}/{png_file}').convert('L')  # Convert mask to grayscale

                # Resize mask to match image size
                mask = mask.resize(image.size)

                # Convert to NumPy arrays
                image_array = np.array(image)
                mask_array = np.array(mask)

                # Normalize and apply mask
                mask_array = mask_array / 255.0
                if len(image_array.shape) == 3:
                    mask_array = np.expand_dims(mask_array, axis=-1)
                masked_image_array = image_array * mask_array

                # Save masked image
                masked_image = Image.fromarray(np.uint8(masked_image_array))
                output_dir = f'/content/Masked_Images/{split_dir[i]}/{directory}'
                os.makedirs(output_dir, exist_ok=True)
                masked_image.save(f'{output_dir}/{jpg_file}')
                masked_image_count += 1
                print(f'Masking {jpg_file} {split_dir[i]} completed - {masked_image_count}')

mask_image(directories)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import scipy
BS = 32
image_size = (224,224)
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=10,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   shear_range=0.1,
                                   zoom_range=0.1,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

valid_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    './Masked_Images/train',
    target_size= image_size,
    batch_size=BS,
    class_mode='categorical',
    color_mode='rgb')

valid_generator = valid_datagen.flow_from_directory(
    './Masked_Images/train',
    target_size= image_size,
    batch_size=BS,
    class_mode='categorical',
    color_mode='rgb')

test_generator = valid_datagen.flow_from_directory(
    './Masked_Images/train',
    target_size= image_size,
    batch_size=BS,
    class_mode='categorical',
    color_mode='rgb')

for _ in range(3):
    img, label = next(train_generator)
    plt.imshow(img[0])
    plt.show()

from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
import os

# Load VGG16 pretrained model
vgg16_model = VGG16(input_shape=(224, 224, 3),
                    include_top=False,
                    weights='imagenet')
vgg16_model.trainable = False  # Freeze the base model

# Build Sequential model
model_vgg16 = Sequential([
    vgg16_model,
    layers.Flatten(),
    layers.Dense(units=1950, activation='relu'),
    layers.BatchNormalization(),
    layers.Dense(units=200, activation='softmax')  # Adjust output for 200 classes
])

# Display the model summary
model_vgg16.summary()

# Compile the model
model_vgg16.compile(
    optimizer=Adam(learning_rate=0.001),  # Specify learning rate
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Define callbacks
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Save the best model during training
os.makedirs('model_checkpoints', exist_ok=True)
model_checkpoint = ModelCheckpoint(
    filepath='model_checkpoints/best_model_vgg16.keras',  # Changed extension to .keras
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)


# Fit the model
history = model_vgg16.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=20,  # Adjust as needed
    verbose=1,
    callbacks=[early_stop, model_checkpoint]
)

# Evaluate the model
test_loss, test_accuracy = model_vgg16.evaluate(test_generator)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

from google.colab import files
import io
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing import image

# Upload image from local machine
uploaded = files.upload()

# Get the uploaded image filename
img_path = next(iter(uploaded))  # The first uploaded file

# Function to prepare the image (resize and normalize)
def prepare_image(img_path, target_size=(224, 224)):
    # Load the image
    img = image.load_img(img_path, target_size=target_size)

    # Convert the image to a numpy array
    img_array = image.img_to_array(img)

    # Rescale the image to [0, 1]
    img_array = img_array / 255.0

    # Add an extra dimension for batch size (as model expects a batch)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array

# Preprocess the uploaded image
processed_img = prepare_image(img_path)

# Make predictions
predictions = model_vgg16.predict(processed_img)

# Get the predicted class index
predicted_class_index = np.argmax(predictions, axis=1)[0]

# Display the image
img = Image.open(img_path)
img.show()

# Get class labels
class_labels = sorted(os.listdir('./Masked_Images/train'))

# Map predicted class index to class label
predicted_class = class_labels[predicted_class_index]

print(f"Predicted Bird Species: {predicted_class}")