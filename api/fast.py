from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import tensorflow.keras as keras
import tensorflow.nn as nn
from deep_pv.params import BUCKET_NAME, MODEL_NAME
import numpy as np

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
    # TODO: make choice select photograph.
    model = keras.models.load_model(f"gs://{BUCKET_NAME}/models/{MODEL_NAME}")
    predict_path = f"gs://{BUCKET_NAME}/data/Rotterdam/PV Present/{latitude}_{longitude}.jpg"
    img = keras.utils.load_img(predict_path, target_size=(256, 256))
    img_array = keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, 0)
    # TODO: make sure this works.
    predictions = model.predict(img_array)
    score = nn.softmax(predictions[0])
    class_name = model.predict_classes
    return {
        'latitude':latitude,
        'longitude':longitude,
        'shape':img_array.shape,
        'class_name':class_name,
        'confidence_interval':100 * np.max(score)
    }
