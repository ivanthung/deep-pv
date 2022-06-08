from pycocotools.coco import COCO
import numpy as np
import os

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
