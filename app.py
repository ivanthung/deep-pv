import streamlit as st
import requests
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

address = st.text_input('Location')

url = 'http://127.0.0.1:8000/predict'

def load_api(url, params):
    r = requests.get(url, params)
    if r.status_code != 200:
        return None
    else:
        return r.json()

if address:
    geolocator = Nominatim(user_agent="http")
    location = geolocator.geocode(address)
    longitude = location.longitude
    latitude = location.latitude

    params = {
        'latitude': latitude,
        'longitude': longitude
    }
    api_outcome = load_api(url,params)
    st.write(api_outcome['response'])

    # array = np.array(api_outcome['picture'])
    # fig = plt.

    image = Image.open(f'{latitude}_{longitude}.jpg')
    st.image(image, caption='Your Location')
