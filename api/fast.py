from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras, nn, expand_dims
from deep_pv.params import BUCKET_NAME, MODEL_NAME
from deep_pv.predict import prediction, download_model2, get_model_locally
import numpy as np
from PIL import Image
import cv2 as cv
import requests
from deep_pv.get_data import get_predict_image_gcp
from google.cloud import storage

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

@app.get("/predict")
def predict(latitude, longitude):
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    picture = requests.get(url,params = {
        'center':f'{round(float(latitude),2)},{round(float(longitude),2)}',
        'zoom':21,
        'size':'640x640',
        'maptype':'satellite',
        'key':'AIzaSyBYmLO0dOqMcbUPTv_A0vKF_DThu0PgK7o'
    })
    picture_stored = cv.cvtColor(cv.imdecode(np.asarray(bytearray(picture.content), dtype="uint8"),cv.IMREAD_COLOR), cv.COLOR_BGR2RGB)
    im = Image.fromarray(picture_stored)
    im.save(f'{latitude}_{longitude}.jpg')
    model = get_model_locally()
    answer = prediction(model, f'{latitude}_{longitude}.jpg')
    return {'response': answer, 'picture': picture_stored.tolist()}
