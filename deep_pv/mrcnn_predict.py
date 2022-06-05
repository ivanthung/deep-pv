#import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import json

import h5py
import tensorflow
import keras
# import clint
# import crontab
# import tablib

#import model from GCP
import os
import pandas as pd
import numpy as np
from google.cloud import storage
from pathlib import Path

ROOT_DIR = os.path.abspath('/home/tobyw/code/ivanthung/deep-pv/')
os.chdir(ROOT_DIR)

MRCNN_DIR = 'deep_pv/mrcnn'
MODEL_DIR = os.path.join(ROOT_DIR + MRCNN_DIR, "logs")
MODEL_WEIGHTS_PATH = 'model_weights_path.h5'

from get_data import get_predict_image_gcp
import skimage

BUCKET_NAME = "wagon-data-907-deeppv"
BUCKET_TRAIN_DATA_PATH = "data/png/"

#import items from the mrcnn model

# Import Mask RCNN
sys.path.append(MRCNN_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import utils
from mrcnn import visualize


#Local directory to reference

class SolarPanelsConfig(Config):
    """Configuration for training on a COCO dataset.
    Derives from the base Config class and overrides values specific
    to the COCO dataset.
    """

    # Give the configuration a recognizable name
    NAME = "solar_panels"

    # Train on 1 GPU and 1 image per GPU. Batch size is 1 (GPUs * images/GPU).
    GPU_COUNT = 1

    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 3  # background + 1 (solar_panels)

    #Dimensions of trainning images are 256x256
    IMAGE_MAX_DIM=256
    IMAGE_MIN_DIM=256

    #Play arround the steps number
    STEPS_PER_EPOCH = 500

    #How often validation is run
    #If not enough space in drive make this number larger
    VALIDATION_STEPS = 5

    #ResNet-50 classifer (pre-trained on MS-COCO)
    BACKBONE = 'resnet50'

    #Using predetermined model values
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)
    TRAIN_ROIS_PER_IMAGE = 32
    MAX_GT_INSTANCES = 50
    POST_NMS_ROIS_INFERENCE = 500
    POST_NMS_ROIS_TRAINING = 1000

class InferenceConfig(SolarPanelsConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    IMAGE_MIN_DIM = 256
    IMAGE_MAX_DIM = 256
    DETECTION_MIN_CONFIDENCE = 0.85

def mrcnn_instantiate():
    config = SolarPanelsConfig(Config)
    inference_config = InferenceConfig()
    # Recreate the model in inference mode
    model = modellib.MaskRCNN(mode="inference",
                          config=inference_config,
                          model_dir=MODEL_DIR)
    #load model_weights to model instatiation
    model.load_weights(MODEL_WEIGHTS_PATH, by_name=True)
    return model

def mrcnn_predict(model, file_name):
    image_path = get_predict_image_gcp(file_name)
    img = skimage.io.imread(image_path)
    img_arr = np.array(img)
    results = model.detect([img_arr], verbose=1)
    r = results[0]
    visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], r['scores'], figsize=(5,5))
    print(r)
    return r

if __name__=='__main__':
    #download_model(BUCKET_NAME)
    # get_model_weights()
    model = mrcnn_instantiate()
    mrcnn_predict(model, '51.906771_4.451552')
