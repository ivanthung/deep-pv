# Import Mask RCNN
from deep_pv.mrcnn.config import Config
from deep_pv.mrcnn import model as modellib
from deep_pv.mrcnn import visualize
import os

#Local directory to reference
from deep_pv.get_data import get_predict_image_gcp, download_weights

# Params
from deep_pv.params import MODEL_NAME, BUCKET_NAME, BUCKET_TRAIN_DATA_CALI
MRCNN_DIR = 'deep_pv/mrcnn'
MODEL_DIR = os.path.join( MRCNN_DIR, "logs")

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
    ''' Instantiate a model in inference mode'''
    inference_config = InferenceConfig()
    model = modellib.MaskRCNN(mode="inference",
                          config=inference_config,
                          model_dir = MODEL_DIR)

    #load model_weights to model instatiation
    weights_path = download_weights()
    model.load_weights(weights_path, by_name=True)
    return model

def mrcnn_predict(model, img):
    img = get_predict_image_gcp(file_name)
    results = model.detect([img], verbose=1)
    r = results[0]
    visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], r['scores'], figsize=(5,5))
    print(r)
    return r

if __name__ == '__main__':
    file_name ='51.906771_4.451552'
    model = mrcnn_instantiate()
    mrcnn_predict(model, '51.906771_4.451552')
