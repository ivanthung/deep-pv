#import packages
import os
import pandas as pd
import numpy as np
from google.cloud import storage
from tensorflow.keras import models
from tensorflow import keras, data
import pathlib

# define basic parameters
batch_size = 16
img_height = 256
img_width = 256

BUCKET_NAME = "wagon-data-907-ward"

from pathlib import Path
def get_images_gcp_train(BUCKET_NAME):
    prefix = 'data/png/'
    dl_dir = 'data/'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        print(blob)
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        directory = "/".join(file_split[0:-1])
        Path(directory).mkdir(parents=True, exist_ok=True)
        print("D",directory)
        blob.download_to_filename(blob.name)

def make_training_dataset():
    # import data from directory
    DATA_DIR = "data/png/"
    #data_dir = tf.keras.utils.get_file('PV01_Rooftop_Brick', untar=False)
    train_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width), batch_size=batch_size)
    val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width), batch_size=batch_size)
    class_names = train_ds.class_names
    AUTOTUNE = data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    print( train_ds, val_ds, class_names)

if __name__ =="__main__":
    #get_images_gcp_train(BUCKET_NAME)
    make_training_dataset()
