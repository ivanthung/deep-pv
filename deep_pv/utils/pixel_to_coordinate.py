import math

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
  ## calculate box
  box = deg2num(lat, long, zoom)
  ## get corners of image
  corners = find_opposite_corners(box, zoom)
  ## calculate latitude and longitude
  lat_y = (y/size)*(corners['bottom_right'][0] - corners['top_left'][0]) + corners['top_left'][0]
  long_x = (x/size)*(corners['bottom_right'][1] - corners['top_left'][1]) + corners['top_left'][1]
  return lat_y, long_x
