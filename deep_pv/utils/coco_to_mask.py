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

def coco_to_mask(filename):
    coco = COCO(filename)
    mask = []
    for ann in coco.dataset['annotations']:
        mask.append(coco.annToMask(ann))
    return mask


if __name__ == '__main__':
    ROOT_DIR = '/Users/ivanthung/code/ivanthung/deep-pv/'
    TEST_RESULTS = 'test_results/'
    os.chdir(ROOT_DIR)

    print(coco_to_mask(TEST_RESULTS + 'test_data.json'))
