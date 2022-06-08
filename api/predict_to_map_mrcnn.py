import numpy as np
from google.cloud import storage
import pydeck as pdk
from deep_pv.utils.results_processing import get_bb_latlon, get_real_mask_area
from deep_pv.params import BUCKET_NAME
from deep_pv.utils.test_output import test_results
from deep_pv.get_data import get_image_names_gcp
import pandas as pd

# # Uncomment when running on intel
# from tensorflow import keras, nn, expand_dims
# from deep_pv.predict import get_model_locally

def make_map(bbs, points):
    """Display a map centered at the mean lat/lon of the query set."""
    # Adding code so we can have map default to the center of the data
    bbs = pd.DataFrame(bbs)
    points = pd.DataFrame(points)

    print(bbs.head())
    midpoint = (np.average(points.lat), np.average(points.lon))

    initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=20)

    layer1 = pdk.Layer(
        "PolygonLayer",
        bbs,
        opacity=1,
        get_polygon="geometry",
        filled=False,
        getLineWidth=.5,
        extruded=False,
        wireframe=True,
        get_line_color=[255,255,0],
        auto_highlight=True,
        pickable=True,
        )

    layer2 = pdk.Layer(
                'ScatterplotLayer',
                data=points,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                minPixelRadius = 10,
                maxPixelRadios = 50,
                get_radius='area',
                stroked=True,
                pickable=True
                )

    #Create labeled map
    labeled_map = pdk.Deck(layers=[layer1,layer2],
                           initial_view_state=initial_view_state,
                           map_style='mapbox://styles/mapbox/satellite-v9')
    labeled_map.to_html('test.html')
    return labeled_map

def prediction_scores(lats, lons, image_names, results='', log = ''):
    """
    Input images to do the prediction on.
    Returns a dictionary of scores with points that have gone through preprocessing,
    that can be spatialized with XY values in the next step.
    """
    # # TODO: once docker file running; implement below logic and replace test results.
    # model = mrcnn_instantiate()
    # results = mrcnn_predict(model, image_names)
    if results == '':
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
            angle_correction_45 =1.8008942047053533
            area_corrected = area*angle_correction_45
            efficiency = 0.15
          ##radiation = get_monthly_average_irr(query) query = {'lat': 51.916667,'lon': 4.5}
            radiation = 88.93895833333335

            kWh_mon = area_corrected*radiation*efficiency
            print(f"Processing result {j} from image: {image_names[i]}")

            if log:
                log.write(f"Loading areas of interest {j} from image: {image_names[i]}")
            scores.append({\
                'name' : image_names[i],
                'score': float(result[0]['scores'][j]),
                'bb_latlon': bb_latlon['bounding box'],
                'lat': float(bb_latlon['midpoint'][0]),
                'lon': float(bb_latlon['midpoint'][1]),
                'area': float(area),
                'area_correction':float(area_corrected),
                'kWh_mon':float(kWh_mon)})
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

def predict_to_map(scores):
    bbs = scores_to_bb(scores)
    points = scores_to_points(scores)
    map = make_map(bbs, points)

    return map

def get_scores(bucket_name,
               prefix ='data/Rotterdam/PV Present/',
               results = '',
               log = ''):

    """"
    Put in bucket name, results file from the prediction.
    Returns a list of lats, lons and preprocessed.
    """

    if log:
        log.write("... getting files from GCP")

    lats, lons, images = get_image_names_gcp(bucket_name,
                                             prefix = prefix)

    scores = prediction_scores(lats, lons, images, results=results, log=log)
    return scores

if __name__=="__main__":
    # TODO: check layertypes PyDeck
    bucket_name = BUCKET_NAME
    scores = get_scores(bucket_name, prefix = 'data/Rotterdam/PV Present/', results = '')
    map = predict_to_map(scores)
    pass
