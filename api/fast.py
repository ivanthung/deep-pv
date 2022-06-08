from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras, nn, expand_dims, Graph
from deep_pv.params import BUCKET_NAME, MODEL_NAME
from deep_pv.mrcnn_predict import mrcnn_instantiate, mrcnn_predict
import numpy as np
from PIL import Image
import cv2 as cv
import requests
from deep_pv.get_data import get_predict_image_gcp, upload_to_gcp
from google.cloud import storage
import tensorflow as tf
import matplotlib.pyplot as plt
import io

graph = tf.get_default_graph()
model = mrcnn_instantiate()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world!"}

## original predict:
# @app.get("/predict")
# def predict(latitude, longitude, key):
#     url = "https://maps.googleapis.com/maps/api/staticmap?"
#     picture = requests.get(url,params = {
#         'center':f'{round(float(latitude),2)},{round(float(longitude),2)}',
#         'zoom':21,
#         'size':'512x512',
#         'maptype':'satellite',
#         'key':key
#     })
#     picture_stored = cv.cvtColor(cv.imdecode(np.asarray(bytearray(picture.content), dtype="uint8"),cv.IMREAD_COLOR), cv.COLOR_BGR2RGB)
#     im = Image.fromarray(picture_stored)
#     im.save(f'{latitude}_{longitude}.jpg')
#     # model = get_model_locally()
#     answer = prediction(model, f'{latitude}_{longitude}.jpg')
#     return {'response': answer, 'picture': picture_stored.tolist()}

@app.get("/predict")
def predict(latitude, longitude):
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    picture = requests.get(url,params = {
        'center':f'{round(float(latitude),6)},{round(float(longitude),6)}',
        'zoom':21,
        'size':'512x512',
        'maptype':'satellite',
        'key':'AIzaSyBYmLO0dOqMcbUPTv_A0vKF_DThu0PgK7o'
    })
    picture_stored = cv.cvtColor(cv.imdecode(np.asarray(bytearray(picture.content), dtype="uint8"),cv.IMREAD_COLOR), cv.COLOR_BGR2RGB)
    im = Image.fromarray(picture_stored)
    upload_to_gcp(im, f'{latitude}_{longitude}')

    temp_bucket_name = BUCKET_NAME
    with graph.as_default():
        r = mrcnn_predict(model, picture_stored)

    for key in r:
        r[key] = r[key].tolist()
    if r['rois']:
        r['solar_present'] = 1
    else:
        r['solar_present'] = 0
    return r
