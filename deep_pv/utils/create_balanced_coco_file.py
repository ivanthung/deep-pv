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

def get_image_with_annotations(im_path, coco_json, catIds):
  images_with_ann = []

  for image_id in range(1, len(os.listdir(im_path))):
    img = coco_json.imgs[image_id]
    anns_ids = coco_json.getAnnIds(imgIds=img['id'], catIds = catIds)

    if anns_ids != []:
      print('storing image with id: ', img['id'])
      anns = coco_json.loadAnns(anns_ids)
      images_with_ann.append(img)
    else:
      print('dumping image with id: ', img['id'])

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
    image_name = im['name']

    image = np.array(Image.open(os.path.join(img_dir, image_name)))
    plt.imsave(dump_location+image_name, image)

    print(f'Dumped {image_name} at {dump_location}')
