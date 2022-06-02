### MLFLOW configuration - - - - - - - - - - - - - - - - - - -

# MLFLOW_URI =
# EXPERIMENT_NAME =

### DATA & MODEL LOCATIONS  - - - - - - - - - - - - - - - - - - -

PATH_TO_LOCAL_MODEL = 'saved_models/class_model'

# TODO BUCKET_TEST_DATA_PATH = "data/test.csv"

# TODO PATH_TO_MODEL = 'models/taxifarepipe/model.joblib'


### GCP configuration - - - - - - - - - - - - - - - - - - -

# /!\ you should fill these according to your account

### GCP Project - - - - - - - - - - - - - - - - - - - - - -

PROJECT_ID = 'deeppv-351812'

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -

BUCKET_NAME = 'wagon-data-907-deeppv'
# Mary's BUCKET_NAME = 'wagon-data-907-ward'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -

# train data file location
# /!\ here you need to decide if you are going to train using the provided and uploaded data/train_1k.csv sample file
# or if you want to use the full dataset (you need need to upload it first of course)

BUCKET_TRAIN_DATA_PATH = 'data/Rotterdam/PV Present'

##### Training  - - - - - - - - - - - - - - - - - - - - - -

IMG_SIZE = 256
BATCH_SIZE = 16

##### Model - - - - - - - - - - - - - - - - - - - - - - - -

# model folder name (will contain the folders for all trained model versions)
MODEL_NAME = 'class_model'

# model version folder name (where the trained model.joblib file will be stored)
# TODO MODEL_VERSION = 'v1'

### GCP AI Platform - - - - - - - - - - - - - - - - - - - -

# not required here

### - - - - - - - - - - - - - - - - - - - - - - - - - - - -
