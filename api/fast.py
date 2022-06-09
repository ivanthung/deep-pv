from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras, nn, expand_dims, Graph
from deep_pv.params import BUCKET_NAME, MODEL_NAME
from deep_pv.mrcnn_predict import mrcnn_instantiate, mrcnn_predict
from deep_pv.utils.pixel_to_coordinate import get_coords, center_input_deg
import numpy as np
from PIL import Image
import cv2 as cv
import requests
from deep_pv.get_data import get_predict_image_gcp, upload_to_gcp, upload_to_gcp_hood
from google.cloud import storage
import tensorflow as tf
import matplotlib.pyplot as plt
import io
from api.predict_to_map_mrcnn import get_scores



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
# def predict(latitude, longitude):
#     url = "https://maps.googleapis.com/maps/api/staticmap?"
#     picture = requests.get(url,params = {
#         'center':f'{round(float(latitude),6)},{round(float(longitude),6)}',
#         'zoom':21,
#         'size':'512x512',
#         'maptype':'satellite',
#         'key':'AIzaSyBYmLO0dOqMcbUPTv_A0vKF_DThu0PgK7o'
#     })
#     picture_stored = cv.cvtColor(cv.imdecode(np.asarray(bytearray(picture.content), dtype="uint8"),cv.IMREAD_COLOR), cv.COLOR_BGR2RGB)
#     im = Image.fromarray(picture_stored)
#     upload_to_gcp(im, f'{latitude}_{longitude}')

#     temp_bucket_name = 'data/Rotterdam/PV Present/'
#     with graph.as_default():
#         results = mrcnn_predict(model, temp_bucket_name)

#     solar_present = 1
#     if len(results) == 0:
#         solar_present = 0

#     return {'results': results,
#             'solar_present': solar_present}

@app.get("/hood")
def hood(latitude, longitude, key, zoom = 21, size = 7):
    graph = tf.get_default_graph()
    model = mrcnn_instantiate()
    latitude, longitude = center_input_deg(float(latitude), float(longitude), zoom)
    latitude, longitude = round(latitude, 6), round(longitude, 6)
    size = int(size)
    zoom = int(zoom)
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    for lat, long in get_coords(latitude, longitude, zoom, size):
        lat, long = round(float(lat),6), round(float(long),6)
        picture = requests.get(url,params = {
            'center':f'{lat},{long}',
            'zoom':str(zoom),
            'size':'512x512',
            'maptype':'satellite',
            'key':key
        })
        picture_stored = cv.cvtColor(cv.imdecode(np.asarray(bytearray(picture.content), dtype="uint8"),cv.IMREAD_COLOR), cv.COLOR_BGR2RGB)
        im = Image.fromarray(picture_stored)
        upload_to_gcp_hood(im, f'{latitude}_{longitude}', f'{lat}_{long}')

    prefix = f'data/hood/{latitude}_{longitude}/'
    with graph.as_default():
        results = mrcnn_predict(model, prefix)
    scores = get_scores(BUCKET_NAME,prefix,results)

    solar_present = 1
    if len(scores) == 0:
        solar_present = 0

    return {'results': scores,
            'solar_present': solar_present}
