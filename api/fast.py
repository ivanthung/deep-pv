from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras, nn, expand_dims
from deep_pv.params import BUCKET_NAME, MODEL_NAME
from deep_pv.predict import prediction, download_model2, get_model_locally
from deep_pv.mrcnn_predict import mrcnn_instantiate, mrcnn_predict
import numpy as np
from PIL import Image
import cv2 as cv
import requests
from deep_pv.get_data import get_predict_image_gcp
from google.cloud import storage

# model = get_model_locally()
model_2 = mrcnn_instantiate()

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
def predict(latitude, longitude, key):
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    picture = requests.get(url,params = {
        'center':f'{round(float(latitude),2)},{round(float(longitude),2)}',
        'zoom':21,
        'size':'512x512',
        'maptype':'satellite',
        'key':key
    })
    picture_stored = cv.cvtColor(cv.imdecode(np.asarray(bytearray(picture.content), dtype="uint8"),cv.IMREAD_COLOR), cv.COLOR_BGR2RGB)
    # im = Image.fromarray(picture_stored)
    # im.save(f'{latitude}_{longitude}.jpg')
    # model = get_model_locally()
    r = mrcnn_predict(model_2, picture_stored)
    # for key in r:
    #     r[key] = r[key].tolist()
    # answer = prediction(model, f'{latitude}_{longitude}.jpg')
    return {'a': 'b'}
