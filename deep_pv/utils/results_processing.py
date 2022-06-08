import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from pycocotools.coco import COCO
from pycocotools import mask
from deep_pv.utils.pixel_to_coordinate import center_to_pixel
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon

def coco_to_mask(filename):
    coco = COCO(filename)
    mask = []
    for ann in coco.dataset['annotations']:
        mask.append(coco.annToMask(ann))
    return mask

def close_contour(contour):
    if not np.array_equal(contour[0], contour[-1]):
        contour = np.vstack((contour, contour[0]))
    return contour

def mask_to_coco(binary_mask, tolerance=0):
    """Converts a binary mask to COCO polygon representation
    from: https://github.com/waspinator/pycococreator/blob/master/LICENSE
    license: Apache License 2.0

    Args:
        binary_mask: a 2D binary numpy array where '1's represent the object
        tolerance: Maximum distance from original points of polygon to approximated
            polygonal chain. If tolerance is 0, the original coordinate array is returned.
    """
    polygons = []
    # pad mask to close contours of shapes which start and end at an edge
    padded_binary_mask = np.pad(binary_mask, pad_width=1, mode='constant', constant_values=0)
    contours = measure.find_contours(padded_binary_mask, 0.5)
    contours = np.subtract(contours, 1)
    for contour in contours:
        contour = close_contour(contour)
        contour = measure.approximate_polygon(contour, tolerance)
        if len(contour) < 3:
            continue
        contour = np.flip(contour, axis=1)
        segmentation = contour.ravel().tolist()
        # after padding and subtracting 1 we may get -0.5 points in our segmentation
        segmentation = [0 if i < 0 else i for i in segmentation]
        polygons.append(segmentation)

    return polygons

def get_real_mask_area(lat, lon, mask):
    return (np.sum(mask) / mask.shape[0] ** 2) * get_tile_area(lat, lon, mask)

def get_tile_area(lat, lon, mask):
    """ TODO: fix this area estimation with haversine distances"""
    tile_area = 256
    return tile_area

def coco_to_cococoords(coco_list):
    """ get list of cococoords, return tuple of coords"""
    return np.array([ [ int(coco_list[c]), int(coco_list[c+1])] for c in range(0, len(coco_list)-1, 2) ])

def get_bb(coco_coords):
    """  Return top left and bottom left value."""
    x = [ x_coord[0] for x_coord in coco_coords]
    y = [ y_coord[1] for y_coord in coco_coords]
    return [(min(x), min(y)), (max(x), max(y))]

def get_bb_latlon(lat: float, lon:float, mask: np.array) -> list:
    """ get mask, return:
    [bounding box: Polygon , midpoint: (x,y)] """
    coco_list = mask_to_coco(mask)[0]
    coco_coords = coco_to_cococoords(coco_list)
    bb = get_bb(coco_coords)
    midpoint = get_midpoint_from_bb(bb)
    midpoint_real_coord = center_to_pixel(lat, lon, midpoint[0], midpoint[1])

    latmin, lonmin = center_to_pixel(lat, lon, *bb[0])
    latmax, lonmax = center_to_pixel(lat, lon, *bb[1])

    return {\
        'bounding box':
                    [[lonmin, latmin],
                    [lonmax,latmin],
                    [lonmax,latmax],
                    [lonmin, latmax]],
        'midpoint': midpoint_real_coord
    }

def get_midpoint_from_bb(bb):
    return np.array(( int((bb[1][0] - bb[0][0])) ,  int((bb[1][1] - bb[0][1])) ))

def test_cococoords(coco_coords, dims = (512, 512)):
    test_array = np.zeros(dims)
    test_array[ tuple(coco_coords.T)] = 1
    plt.imshow(test_array)
    plt.show()

def main():
    ROOT_DIR = '/Users/ivanthung/code/ivanthung/deep-pv/'
    TEST_RESULTS = 'test_results/'

    mask = coco_to_mask(TEST_RESULTS + 'test_data.json')

    coco_list = mask_to_coco(mask[0])[0]
    coco_coords = coco_to_cococoords(coco_list)
    bb = get_bb(coco_coords)
    midpoint = get_midpoint_from_bb(bb)
    midpoint_real_coord = center_to_pixel(51.912667, 4.478559, midpoint[0], midpoint[1])

    print(midpoint_real_coord)
    crs = {'init': 'epsg:4326'}
    polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=midpoint_real_coord)

    polygon.to_file(filename='test_results/polygon_test.geojson', driver='GeoJSON')
    polygon.to_file(filename='test_results/polygon_test.shp', driver="ESRI Shapefile")

if __name__ == '__main__':
    main()
