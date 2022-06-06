import streamlit as st
import requests
from geopy.geocoders import Nominatim
from PIL import Image
from api.predict_to_map import get_images_gcp, get_model_locally, make_dataset, make_map, prediction_map
from deep_pv.params import BUCKET_NAME

# @st.cache
lat, lon, image_name = get_images_gcp(BUCKET_NAME)
model = get_model_locally()
image_class, heat_score_list = prediction_map(model, image_name)
image_dataset = make_dataset(image_class, heat_score_list,lat, lon, image_name)

clicked = st.button('Click for heat map')

if clicked:
    st.pydeck_chart(make_map(image_dataset))

address = st.text_input('Location')
key = st.text_input('API Key')

url = 'http://127.0.0.1:8000/predict'

def load_api(url, params):
    r = requests.get(url, params)
    if r.status_code != 200:
        return None
    else:
        return r.json()

if address and key:
    geolocator = Nominatim(user_agent="http")
    location = geolocator.geocode(address)
    longitude = location.longitude
    latitude = location.latitude

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'key':key
    }
    api_outcome = load_api(url,params)
    st.write(api_outcome['response'])

    image = Image.open(f'{latitude}_{longitude}.jpg')
    st.image(image, caption='Your Location')
