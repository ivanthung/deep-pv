import numpy as np
from google.cloud import storage
import pydeck as pdk
from deep_pv.utils.results_processing import get_bb_latlon, get_real_mask_area
from deep_pv.params import BUCKET_NAME
from deep_pv.utils.test_output import test_results
import streamlit as st
import pandas as pd
import geopandas as gpd

# # Uncomment when running on intel
# from tensorflow import keras, nn, expand_dims
# from deep_pv.predict import get_model_locally

def get_images_gcp(BUCKET_NAME, prefix = 'data/Rotterdam/PV Present/'): #change to include variable for filename
    """" Inputs bucket name and prefix path from root of bucket:
    example: data/Rotterdam/PV_Present
    returns: lat, lon, and image names in a list fomr the"""

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    print("Bucket name: ", bucket)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    lats = []
    lons = []
    image_names = []
    for blob in blobs:
        name = blob.name[-22:]
        name = 'data/'+ name
        lat = blob.name[-22:-13].replace('_', '')
        lon = blob.name[-12:-4].replace('_', '')
        lats.append(float(lat))
        lons.append(float(lon))
        image_names.append(name)
        blob.download_to_filename(name) #filename = 'data/lat_lon.jpg'
    return lats, lons, image_names

def make_map(lats, lons, bbs, points):
    """Display a map centered at the mean lat/lon of the query set."""
    # Adding code so we can have map default to the center of the data
    midpoint = (np.average(lats), np.average(lons))

    initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=11)

    layer1 = pdk.Layer(
        "PolygonLayer",
        pd.DataFrame(bbs),
        opacity=0.8,
        get_polygon="geometry",
        filled=False,
        extruded=False,
        get_line_color=[255, 255, 255],
        auto_highlight=True,
        pickable=True,
        )

    layer2 = pdk.Layer(
                'ScatterplotLayer',
                data=pd.DataFrame(points),
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
                )

    #Create labeled map
    labeled_map = pdk.Deck(layers=[layer1, layer2],
                           initial_view_state=initial_view_state,
                           map_style='mapbox://styles/mapbox/light-v9')

    return labeled_map

def prediction_scores(lats, lons, image_names, log = ''):
    """
    Input images to do the prediction on.
    Returns a dictionary of scores with points that have gone through preprocessing,
    that can be spatialized with XY values in the next step.
    """
    # # TODO: once docker file running; implement below logic and replace test results.
    # model = mrcnn_instantiate()
    # results = mrcnn_predict(model, image_names)

    results = test_results()
    scores = []
    for i, result in enumerate(results):
        n_annotations = len(result[0]['class_ids'])
        for j in range(n_annotations):
            mask = result[0]['masks'][:,:,j]
            bb_latlon = get_bb_latlon(lats[i], lons[i], mask)

            if log:
                log.write(f"Loading areas of interest {j} from image: {image_names[i]}")

            scores.append({\
                'name' : image_names[i],
                'mask': mask,
                'score': result[0]['scores'][j],
                'bb_latlon': bb_latlon['bounding box'],
                'lat': bb_latlon['midpoint'][0],
                'lon': bb_latlon['midpoint'][1],
                'area': get_real_mask_area(lats[i], lons[i], mask)})
    return scores

def scores_to_points(scores):
    return [{
        'name': s['name'],
        'lat': s['lat'],
        'lon': s['lon'],
        'area': s['area']
        } for s in scores ]

def scores_to_bb(scores):
    return [{
        'name': s['name'],
        'geometry': s['bb_latlon'],
        'confidence': s['score']
        } for s in scores ]

def scores_to_shape(scores):
    pass

def predict_to_map(lats, lons, scores):
    bbs = scores_to_bb(scores)
    points = scores_to_points(scores)
    map = make_map(lats, lons, bbs, points)

    print(pd.DataFrame(bbs).head())
    return map

def get_scores(bucket_name, log = ''):
    if log:
        log.write("... getting files from GCP")

    lats, lons, images = get_images_gcp(bucket_name)
    scores = prediction_scores(lats, lons, images, log=log)
    return lats, lons, scores

if __name__=="__main__":
    # TODO: check layertypes PyDeck
    bucket_name = BUCKET_NAME
    lats, lons, scores = get_scores(bucket_name)
    map = predict_to_map(lats, lons, scores)
    pass
