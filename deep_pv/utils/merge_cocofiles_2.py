import json
from pathlib import Path
import os
from pycocotools.coco import COCO
import numpy as np

# BASE_DIR = Path(__file__).resolve(strict=True).parent


BASE_DIR = Path('/Users/ivanthung/code/ivanthung/deep-pv/data/cocojson')
IMAGES_DIR = Path('/Users/ivanthung/code/ivanthung/deep-pv/data/geo_balanced')
OUTPUT_NAME = BASE_DIR / "COCO_merge_test.json"

def create_coco(annotations, images):
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
    "categories": categories
    }

def test_coco_file():
    coco_json = COCO(OUTPUT_NAME)
    print("Checking validadity of notations")
    no_anns = []

    for imId in coco_json.getImgIds():
        anns = coco_json.getAnnIds(imgIds=imId, catIds = [1])
        if anns == '[]':
            no_anns.append(imId)

    for image in coco_json.dataset['images']:
        print("testing if image exists: ", image['file_name'])
        path = os.path.join(IMAGES_DIR, image['file_name'])
        assert os.path.exists(path)

    print(f"summary of:", OUTPUT_NAME)
    print(f"Images: {no_anns} have no annotations")
    print(f"{len(no_anns)} images without annotations")
    print("Amount of images loaded: ", len(coco_json.dataset['images']))
    print("Amount of IDs = ", len(coco_json.getImgIds()))
    print("Amount of AnnIds = ", len(coco_json.getAnnIds()))
    print("Unique AnnIds = ", len(np.unique(coco_json.getAnnIds())))

def create_temp_id_field(data: list, field_name: str, the_type: str ):
    for image in data:
        image["temp_id"] = f"{the_type}_{image[field_name]}"
    return data

def make_json():
    with open(BASE_DIR / "COCO_china_concrete.json") as json_file:
        steel_data = json.load(json_file)
    with open(BASE_DIR / "COCO_china_steel.json") as json_file:
        brick_data = json.load(json_file)

    images = create_temp_id_field(
        steel_data["images"], "id", "s"
    ) + create_temp_id_field(brick_data["images"], "id", "b")

    annotations = create_temp_id_field(
        steel_data["annotations"], "image_id", "s"
    ) + create_temp_id_field(brick_data["annotations"], "image_id", "b")

    for index, image in enumerate(images, 1):
        image["id"] = index

    for annotation in annotations:
        try:
            annotation["image_id"] = list(
                filter(lambda x: x["temp_id"] == annotation["temp_id"], images)
            )[0]["id"]
        except:
            print("image out of range", annotation["temp_id"])
        del annotation["temp_id"]

    for image in images:
        del image["temp_id"]

    merged = create_coco(annotations, images)

    print("no images", len(images))
    with open(OUTPUT_NAME, 'w') as fp:
        json.dump(merged, fp)

if __name__ == "__main__":
    make_json()
    test_coco_file()
