import math
import numpy as np

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def find_corners(tile, zoom=21):
  return {
      'top_left':num2deg(tile[0], tile[1], zoom),
      'top_right':num2deg(tile[0]+1, tile[1], zoom),
      'center':num2deg(tile[0]+0.5, tile[1]+0.5, zoom),
      'bottom_left':num2deg(tile[0], tile[1]+1, zoom),
      'bottom_right':num2deg(tile[0]+1, tile[1]+1, zoom)
  }

def find_opposite_corners(tile, zoom = 21):
  return {'top_left':num2deg(tile[0], tile[1], zoom),
          'bottom_right':num2deg(tile[0]+1, tile[1]+1, zoom)}

## function below requires image to have centre as centre of standard 512x512 zoom 21.
def center_to_pixel(lat, long, x, y, size = 512, zoom = 21):
    """ Input:
    lat: center coordinate
    long: center coordinate
    x: pixel coordinate x
    y: pixel coordinate y
    returns lat_y, lon_x
    """

    box = deg2num(lat, long, zoom)
    ## get corners of image
    corners = find_opposite_corners(box, zoom)
    ## calculate latitude and longitude
    lat_y = (y/size)*(corners['bottom_right'][0] - corners['top_left'][0]) + corners['top_left'][0]
    long_x = (x/size)*(corners['bottom_right'][1] - corners['top_left'][1]) + corners['top_left'][1]
    return lat_y, long_x

def get_coords(lat_deg, lon_deg, zoom = 21, size = 30):
  (x,y) = deg2num(lat_deg, lon_deg, zoom)
  return (np.array([num2deg(x + i - size//2,
                            y + j - size//2, zoom)
                            for j in range(size)
                            for i in range(size)])
                            .reshape(size,size,2))

def get_coords_list(lat_deg, lon_deg, zoom = 21, size = 7):
  (x,y) = deg2num(lat_deg, lon_deg, zoom)
  return ([num2deg(x + i - size//2,
            y + j - size//2, zoom)
            for j in range(size)
            for i in range(size)])

def haversine_vectorized(start_lat,
                         start_lon,
                         end_lat,
                         end_lon):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees).
        Vectorized version of the haversine distance for pandas df
        Computes distance in kms
    """

    lat_1_rad, lon_1_rad = np.radians(start_lat.astype(float)),\
        np.radians(start_lon.astype(float))
    lat_2_rad, lon_2_rad = np.radians(end_lat.astype(float)),\
        np.radians(end_lon.astype(float))
    dlon = lon_2_rad - lon_1_rad
    dlat = lat_2_rad - lat_1_rad

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) *\
        np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c
