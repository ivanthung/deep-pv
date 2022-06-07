import os
import pandas as pd
import numpy as np
from google.cloud import storage
from tensorflow.keras import models
#from deep_pv.get_data import get_predict_image_gcp
#from keras.applications.utils import load_img, img_to_array
from tensorflow import keras, nn, expand_dims
#PATH_TO_LOCAL_MODEL = 'model.joblib'

BUCKET_NAME = "wagon-data-907-deeppv"  # ⚠️ replace with project BUCKET NAME

## download model from GCP
# def download_model(bucket=BUCKET_NAME):
#     client = storage.Client().bucket(bucket)
#     storage_location = 'models/class_model/saved_model.pb'
#     print(storage_location)
#     blob = client.blob(storage_location)
#     blob.download_to_filename('model.joblib')
#     print(blob)
#     print("=> pipeline downloaded from storage")
#     model = models.load_model('model.pb')
#     # if rm:
#     #     os.remove('model.pb')
#     return model

from pathlib import Path
def download_model2(BUCKET_NAME):
    prefix = 'models/class_model/'
    dl_dir = 'class_model/'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        directory = "/".join(file_split[0:-1])
        Path(directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(blob.name)


## source model locally saved
def get_model_locally():
    model = models.load_model('models/class_model')
    return model

## predict model with imported model

def prediction(model, predict_path = '105.jpg'):
    img = keras.utils.load_img(predict_path, target_size=(256, 256))
    img_array = keras.utils.img_to_array(img)
    img_array = expand_dims(img_array, axis = 0)
    # Create a batch
    predictions = model.predict(img_array)
    score = nn.softmax(predictions[0])
    decoder = {0:'less_0',1: 'less_10', 2:'less_5', 3:'more_10'}
    class_name = predictions.argmax(axis=-1)[0]
    class_name = decoder[class_name]
    print("max_score",np.argmax(score))
    return "This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_name, 100 * np.max(score))

if __name__ == '__main__':
    # model = download_model2(BUCKET_NAME)
    model = get_model_locally()
    print(prediction(model, predict_path = '51.906771_4.451552.jpg'))
