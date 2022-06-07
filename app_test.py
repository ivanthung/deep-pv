import streamlit as st
import requests
from geopy.geocoders import Nominatim
from PIL import Image
from api.predict_to_map_mrcnn import get_scores, predict_to_map
from deep_pv.params import BUCKET_NAME

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
    col1.metric(label="Temperature", value="70 °F", delta="1.2 °F")

bucket_name = BUCKET_NAME
lats, lons, scores = get_scores(bucket_name, log=col2)
map = predict_to_map(lats, lons, scores)

if clicked:
    col1.pydeck_chart(map)

# def load_api(url, params):
#     r = requests.get(url, params)
#     if r.status_code != 200:
#         return None
#     else:
#         return r.json()

# display_basemap()

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
