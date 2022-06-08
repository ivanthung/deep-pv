import streamlit as st
import requests
from geopy.geocoders import Nominatim
from PIL import Image
from api.predict_to_map_mrcnn import prediction_scores #, get_scores, predict_to_map, get_images_gcp
from deep_pv.params import BUCKET_NAME
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
import pydeck as pdk

URL = 'http://127.0.0.1:8000/predict'

# @st.cache
# predict all images to a bucket and return the stuff.
st.set_page_config(layout="wide")
col1, col2 = st.columns((4, 1))
col2.header("Logs")
col1.header("DEEP-PV")
col1.markdown("Get solar panel stats from any place in the world. \n 1. Define location. \n 2. Add API key.")

clicked = col1.button('Click for heat map')
kpi = col1.button('Generate KPIs')

address = col1.text_input('Location')
key = col1.text_input('API Key')
url = 'http://127.0.0.1:8000/predict'


if kpi:
    # bucket_name = BUCKET_NAME
    # lats, lons, image_names = get_images_gcp(BUCKET_NAME, prefix = 'data/Rotterdam/PV Present/')
    scores_dict = prediction_scores()#lats, lons, image_names?
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.hist(pd.DataFrame(scores_dict)['kWh_mon'].apply(round), bins = 20)
    plt.title("Distribution of power output per panel detected")
    plt.xlabel('kWh per Month output')
    plt.ylabel('Frequency')
    plt.show()
    col1.pyplot(fig)
    df = pd.DataFrame(scores_dict)
    total_energy_output = df['kWh_mon'].sum().round()
    total_num_PV = len(df)
    average_energy_output = df['kWh_mon'].mean().round()



# def load_api(url, params):
#     r = requests.get(url, params)
#     if r.status_code != 200:
#         return None
#     else:
#         return r.json()

# if address and key:
#     geolocator = Nominatim(user_agent="http")
#     location = geolocator.geocode(address)
#     longitude = location.longitude
#     latitude = location.latitude

#     params = {
#         'latitude': latitude,
#         'longitude': longitude,
#         'key':key
#     }
#     api_outcome = load_api(url,params)
#     st.write(api_outcome['response'])

#     image = Image.open(f'{latitude}_{longitude}.jpg')
#     st.image(image, caption='Your Location')
