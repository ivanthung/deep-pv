#import packages
import os
import pandas as pd
import numpy as np
from google.cloud import storage
from tensorflow.keras import models
from tensorflow import keras, nn, expand_dims
from pathlib import Path
import streamlit as st
from deep_pv.predict import get_model_locally
import pydeck as pdk

BUCKET_NAME = "wagon-data-907-deeppv"

@st.cache
def get_images_gcp(BUCKET_NAME): #change to include variable for filename
    prefix = f'data/Rotterdam/PV Present/' #without coordinants
    dl_dir = 'rotterdam_mary/'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    print(bucket)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    print(blobs)
    lats = []
    lons = []
    image_name = []
    for blob in blobs:
        name = blob.name[-22:]
        name = 'data/'+ name
        lat = blob.name[-22:-13]
        lon = blob.name[-12:-4]
        lats.append(lat)
        lons.append(lon)
        image_name.append(name)
        blob.download_to_filename(name) #filename = 'data/lat_lon.jpg'
    return lats, lons, image_name

def prediction_map(model, image_name):
    image_class = []
    heat_score_list = []
    for path in image_name:
      img = keras.utils.load_img(path, target_size=(256, 256))
      img_array = keras.utils.img_to_array(img)
      img_array = expand_dims(img_array, axis = 0)
      predictions = model.predict(img_array)
      score = nn.softmax(predictions[0])
      decoder = {0:'less_0',1: 'less_10', 2:'less_5', 3:'more_10'}
      heat_map_score = {'less_0':0,'less_10':2,'less_5':1, 'more_10':3}
      class_name = predictions.argmax(axis=-1)[0]
      class_name = decoder[class_name]
      heat_score = heat_map_score[class_name]
      image_class.append(class_name)
      heat_score_list.append(heat_score)
      result_statement = "This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_name, 100 * np.max(score))
    return image_class, heat_score_list, result_statement

def make_dataset(image_class, heat_score_list,lat, lon, image_name):
    image_dataset = pd.DataFrame({"image_name": image_name, "image_class": image_class , "heat_score_list":heat_score_list, "lat":lat, "lon":lon})
    return image_dataset

def make_map(image_dataset):
    """Display a map centered at the mean lat/lon of the query set."""
    # Adding code so we can have map default to the center of the data
    image_dataset['lat'] = image_dataset['lat'].astype('float')
    image_dataset['lon'] = image_dataset['lon'].astype('float')
    midpoint = (np.average(image_dataset['lat']), np.average(image_dataset['lon']))

    initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=11)


    layer1= pdk.Layer(
                'HexagonLayer',
                data=image_dataset,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True )

    layer2 = pdk.Layer(
                'ScatterplotLayer',
                data= image_dataset,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=40)

    #Render
    labeled_map = pdk.Deck(layers=[layer2], initial_view_state=initial_view_state)
    return labeled_map



if __name__=="__main__":
    lat,lon, image_name = get_images_gcp(BUCKET_NAME)
    model = get_model_locally()
    image_class, heat_score_list, result_statement = prediction_map(model, image_name)
    image_dataset = make_dataset(image_class, heat_score_list,lat, lon, image_name)
