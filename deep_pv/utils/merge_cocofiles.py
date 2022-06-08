import os
from results_processing import mask_to_coco
import json

ROOT = '/Users/ivanthung/code/ivanthung/deep-pv/'
JSON_OUTPUT = 'data/PV01/cocojson/'

filenames = os.listdir(ROOT + JSON_OUTPUT)

if __name__ == "__main__":
    print(filenames)
    scalar = [90, 90, 90]
    scale = {file: scalar[i] for i, file in enumerate(filenames)}
    images = []
    annotations = []
    image_counter, annotation_counter = 0,0
    for file, scalar in scale.items():

        with open(JSON_OUTPUT + file) as json_file:
            file_data = json.load(json_file)
        for i in range(scalar):
            images.append(\
                {   image_counter :
                    [file,
                    file_data['images'][i]['id'],
                    file_data['images']]
                    })
            image_counter +=1

    print(images)

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


"""
list of filepaths.


Get image paths.
Decide on proportions of images.
Set default Info and License.

open files as json in files as list of json in huge mf list.

Get-images
load all images of coco1 in a dict with an ID
filenames
for file in files:
    while IDnew < min(len(figures), no_images)
        IDnew : [file1+imageID, image] -> coco1
        IDnew++

In a second loop.
Annotationcounter = 0
for each [file] in IDnew.values()
    IDnew : [file1+ID, image] -> annotation.

images = re-map(images)
annotations = re-map(annotations)

Dump files in merged folder.


"""
