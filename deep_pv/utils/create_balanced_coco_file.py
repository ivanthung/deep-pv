import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
from pycocotools.coco import COCO
import os
from os import path
import json

def get_image_with_annotations(im_path, coco_json, catIds = [1]):
  images_with_ann = []
  every_other = 0

  for image_id in coco_json.getImgIds():
    try:
        img = coco_json.imgs[image_id]
        anns_ids = coco_json.getAnnIds(imgIds=img['id'], catIds = catIds)

        if anns_ids != []:
            print('checking potential image with id: ', img['id'])
            try:
                image = np.array(Image.open(os.path.join(im_path, img['file_name'])))
                print('adding image with annotation :', img['id'])
                images_with_ann.append(img)
                every_other += 1
            except: print(f"image {img['id']} doesn't exist")

        elif (every_other % 2):
            try:
                image = np.array(Image.open(os.path.join(im_path, img['file_name'])))
                print('adding image without annotation :', img['id'])
                images_with_ann.append(img)
            except: print(f"image {id} doesn't exist")

        else:
            print('getting rid of image with id: ', img['id'])

    except:
        print("errored on image with id ", image_id)

  return images_with_ann

def filter_coco_file(coco_path, im_path, catIds = [1]):
  print(coco_path)
  coco_json = COCO(coco_path)

  print("amount images before filtering", len(coco_json.dataset['images']))
  print(f"IMpath: {im_path}, cocopath: {coco_path}, catIds: {catIds}")
  print("amount images after filtering", len(get_image_with_annotations(im_path, coco_json, catIds)))

  info = {
    "description": "Cali Dataset FULL filtered on images with panels",
    "url": "https://www.nature.com/articles/sdata2016106",
    "version": "1.0",
    "year": 2016,
    "contributor": "original from nature, created by Ivan Thung",
    "date_created": "2016/09/01"
    }

  licenses = [
    {
        "url": "https://creativecommons.org/licenses/by/4.0/",
        "id": 1,
        "name": "Creative Commons Attribution 4.0 International License"
    }]

  return {
      "info" : info,
      "images": get_image_with_annotations(im_path, coco_json, catIds),
      "annotations": coco_json.dataset['annotations'],
      "categories": coco_json.dataset['categories'],
      "licenses": licenses
      }

def dump_images(img_dir, dump_location, coco_path):
  """ Dump all images from a coco into another path"""
  coco_json = COCO(coco_path)
  for im in coco_json.dataset['images']:
    image_name = im['file_name']

    image = np.array(Image.open(os.path.join(img_dir, image_name)))
    plt.imsave(dump_location+image_name, image)

    print(f'Dumped {image_name} at {dump_location}')

def main():
    coco_filepath = DATA_DIR
    coco_filename = ['COCO_all_fresno_split.json']
    coco_filename_out = 'COCO_all_fresno_balanced.json'
    dump_location = 'cocofiles_all_fresno_balanced/'
    file_dim = (256, 256, 3)

    os.makedirs(ALL_DATA_DIR + dump_location, exist_ok=True)
    print(f"The new directory {dump_location} is created!")

    all_files = os.listdir(DATA_DIR)
    for file in all_files:
        if file.endswith('.json'):
            print("Found my JSON: ", file)

    balanced_coco_file = filter_coco_file(DATA_DIR + coco_filename[0], coco_filepath, [1])
    with open(ALL_DATA_DIR + coco_filename_out, 'w') as fp:
        json.dump(balanced_coco_file, fp)

    print("dumped balanced JSON file")

    dump_images(DATA_DIR, ALL_DATA_DIR + dump_location, ALL_DATA_DIR + coco_filename_out)
    print("finished dumping!")

def test_coco_file():
    coco_json = COCO(ALL_DATA_DIR + 'COCO_all_fresno_balanced.json')
    print("Checking validadity of notations")
    for imId in coco_json.getImgIds():
        print("testing image with ID ", imId)
        assert coco_json.getAnnIds(imgIds=imId, catIds = [1]) != []
    for image in coco_json.dataset['images']:
        assert os.path.exists(OUTPUT_DATA_DIR + image['file_name'])

    print("Amount of images loaded: ", len(coco_json.dataset['images']))


if __name__ == '__main__':
    ROOT_DIR = '/Users/ivanthung/code/ivanthung/deep-pv/'
    DATA_DIR = 'raw_data/cocofiles_fresno/'
    OUTPUT_DATA_DIR = 'raw_data/cocofiles_all_fresno_balanced/'
    ALL_DATA_DIR = 'raw_data/'

    os.chdir(ROOT_DIR)
    test_coco_file()
    # main()
