### DATA & MODEL LOCATIONS  - - - - - - - - - - - - - - - - - - -

PATH_TO_LOCAL_MODEL = 'saved_models/class_model'
# TODO BUCKET_TEST_DATA_PATH = "data/test.csv"
# TODO PATH_TO_MODEL = 'models/taxifarepipe/model.joblib'

### GCP configuration - - - - - - - - - - - - - - - - - - -
### GCP Project - - - - - - - - - - - - - - - - - - - - - -

PROJECT_ID = 'deeppv-351812'

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -
BUCKET_NAME = 'wagon-data-907-deeppv'
# Mary's BUCKET_NAME = 'wagon-data-907-ward'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -
BUCKET_TRAIN_DATA_PATH = 'data/Rotterdam/PV Present'
BUCKET_TRAIN_DATA_CHINA = 'train_data/data/PV01/PV01_Rooftop_Brick/'
BUCKET_TRAIN_DATA_CALI = 'train_data/data/Cali/cocofiles_all_stockton_balanced'

##### Training  - - - - - - - - - - - - - - - - - - - - - -
IMG_SIZE = 256
BATCH_SIZE = 16

##### Model - - - - - - - - - - - - - - - - - - - - - - - -
# model folder name (will contain the folders for all trained model versions)
MODEL_NAME = 'class_model'

### LOCAL PATHS
WEIGHTS_PATH = 'models/trained_weights/'
