import numpy as np
from google.cloud import storage
import pydeck as pdk
from deep_pv.utils.results_processing import get_bb_latlon, get_real_mask_area
from deep_pv.params import BUCKET_NAME
from deep_pv.utils.test_output import test_results
import streamlit as st
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
    layer1= pdk.Layer(
                'ShapeLayer',
                data=bbs,
                get_position='[lon, lat]',
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True )
    layer2 = pdk.Layer(
                'ScatterplotLayer',
                data=points,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=40)
    #Render
    labeled_map = pdk.Deck(layers=[layer2], initial_view_state=initial_view_state)
    return st.pydeck_chart(labeled_map)

def prediction_scores(lats, lons, image_names):
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
          ##area_tile = get_tile_area(lat, lon, mask)
            area_tile = 256
            area = (np.sum(mask) / mask.shape[0] ** 2) * area_tile
          ##angel_correction_45 = get_angle(0.45)
            angel_correction_45 =1.8008942047053533
            area_corrected = area*angel_correction_45
            efficiency = 0.15
          ##radiation = get_monthly_average_irr(query) query = {'lat': 51.916667,'lon': 4.5}
            radiation = 88.93895833333335
            kWh_mon = area_corrected*radiation*efficiency
            print(f"Processing result {j} from image: {image_names[i]}")
            scores.append({\
                'name' : image_names[i],
                'mask': mask,
                'score': result[0]['scores'][j],
                'bb_latlon': bb_latlon['bounding box'],
                'lat': bb_latlon['midpoint'][0],
                'lon': bb_latlon['midpoint'][1],
                'area': area,
                'area_correction':area_corrected,
                'kWh_mon':kWh_mon})
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

def predict_to_map(bucket_name):
    lats, lons, images = get_images_gcp(bucket_name)
    scores = prediction_scores(lats, lons, images)

    df = gpd.GeoDataFrame(scores)
    print(df.head())
    # bbs = scores_to_bb(scores)
    # points = scores_to_points(scores)
    # map = make_map(lats, lons, bbs, points)
    return map

if __name__=="__main__":
    # TODO: check layertypes PyDeck
    bucket_name = BUCKET_NAME
    predict_to_map(bucket_name)
    pass
