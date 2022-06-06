import pandas as pd
import numpy as np
from google.cloud import storage
import pydeck as pdk
from deep_pv.params import BUCKET_NAME
from deep_pv.utils.test_output import test_results

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
        lat = blob.name[-22:-13]
        lon = blob.name[-12:-4]
        lats.append(lat)
        lons.append(lon)
        image_names.append(name)
        blob.download_to_filename(name) #filename = 'data/lat_lon.jpg'
    return lons, lats, image_names

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
    return st.pydeck_chart(labeled_map)

def prediction_map_mrcnn(lons, lats, image_names):
    """
    Input images to do the prediction on.
    Returns a dictionary of scores and shapes that have gone through preprocessing,
    that can be spatialized with XY values in the next step.
    """

    # # TODO: once docker file running; implement below logic and replace test results.
    # model = mrcnn_instantiate()
    # results = mrcnn_predict(model, image_names)
    print("Loading images from: ", image_names)
    results = test_results()


    pass

def test_ivan():
    prediction_map_mrcnn(get_images_gcp(BUCKET_NAME))


    # image_dataset = make_dataset(image_class, heat_score_list,lat, lon, image_name)
    return

if __name__=="__main__":
    test_ivan()
    pass
