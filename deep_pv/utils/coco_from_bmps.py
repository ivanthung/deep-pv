import os
from results_processing import mask_to_coco
import matplotlib.pyplot as plt
import numpy as np
from pycocotools import mask as cocomask
from pycocotools.coco import COCO
import json

ROOT = '/Users/ivanthung/code/ivanthung/deep-pv/'
images = 'data/PV01/PV01_Rooftop_SteelTile'

JSON_OUTPUT = 'data/PV01/'
OUTPUT_NAME = 'COCO_china_steel.json'

IMAGES_DIR = os.path.join(ROOT, images)
IM_DIMS = 256

assert os.path.exists(IMAGES_DIR)

def get_im_ids():
    all_files = os.listdir(IMAGES_DIR)
    all_files= sorted(all_files)
    i, im_ids = 1, {}

    for j in range(0, len(all_files) -1, 2):
        im_ids[i] = [all_files[j], all_files[j+1]]
        i += 1
    return im_ids

def get_bb(ann):
    """  The COCO bounding box format is [top left x position, top left y position, width, height]."""
    x = [ ann[i] for i in range(0, len(ann) - 1, 2) ]
    y = [ ann[i+1] for i in range(0, len(ann) - 1, 2) ]
    return [min(x), min(y), max(x)-min(x), max(y)-min(y)]

def get_area(ann):
    RLEs = cocomask.frPyObjects([ann], IM_DIMS, IM_DIMS)
    RLE = cocomask.merge(RLEs)
    return cocomask.area(RLE)

def get_anns(im_ids):
    annotation_counter = 0
    annotations = []

    for id, mask in im_ids.items():
        mask_file = im_ids[id][1]
        mask = plt.imread(IMAGES_DIR +'/'+ mask_file)
        anns = mask_to_coco(mask)

        for ann in anns:
            annotations.append({
                "segmentation": ann,
                "area": int(get_area(ann)),
                "iscrowd": 0,
                "image_id": id,
                "bbox": get_bb(ann),
                "category_id": 1,
                "id": annotation_counter +1
                })
            annotation_counter += 1
    return annotations

def get_images(im_ids):
    return [{
          "license": 1,
          "file_name": filenames[0],
          "height": 256,
          "width": 256,
          "id": id
          } for id, filenames in im_ids.items()
          ]

    return images

def create_coco():
    im_ids = get_im_ids()
    annotations = get_anns(im_ids)
    images = get_images(im_ids)

    info = {
    "description": "PV-01 steel - converted to COCO by Ivan Thung",
    "url": "https://essd.copernicus.org/preprints/essd-2021-270/essd-2021-270.pdf",
    "version": "1",
    "year": 2016,
    "contributor": "....",
    "date_created": "2022/06/07"
    }

    licenses = [
    {
        "url": "https://creativecommons.org/licenses/by/4.0/",
        "id": 1,
        "name": "Creative Commons Attribution 4.0 International License"
    }]

    categories =  [
    {"supercategory": "panel","id": 1,"name": "panel"},
    {"supercategory": "background","id": 2,"name": "background"}]

    return {
    "info": info,
    "licenses": licenses,
    "images": images,
    "annotations": annotations,
    "categories": categories, # Not in Captions annotations
    }

def test_coco_file():
    coco_json = COCO(ROOT + JSON_OUTPUT + OUTPUT_NAME)
    print("Checking validadity of notations")

    for imId in coco_json.getImgIds():
        print("testing if image has annotation ", imId)
        print(coco_json.getAnnIds(imgIds=imId, catIds = [1]))

    for image in coco_json.dataset['images']:
        print("testing if image exists: ", image['file_name'])
        path =os.path.join(IMAGES_DIR, image['file_name'])
        assert os.path.exists(path)
    print("Amount of images loaded: ", len(coco_json.dataset['images']))

def main():
    coco = create_coco()
    with open(ROOT + JSON_OUTPUT + OUTPUT_NAME, 'w') as fp:
        json.dump(coco, fp)
        print("dumped cocofile ")

if __name__ == '__main__':
    # main()
    test_coco_file()
