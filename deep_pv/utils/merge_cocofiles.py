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
