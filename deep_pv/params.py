
##path for drive

PATH_TO_LOCAL_MODEL = 'saved_models/class_model'

AWS_BUCKET_TEST_PATH = "s3://wagon-public-datasets/taxi-fare-test.csv"


### GCP configuration - - - - - - - - - - - - - - - - - - -

# /!\ you should fill these according to your account

### GCP Project - - - - - - - - - - - - - - - - - - - - - -

# not required here

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -

BUCKET_NAME = 'wagon-data-907-ward'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -

# train data file location
# /!\ here you need to decide if you are going to train using the provided and uploaded data/train_1k.csv sample file
# or if you want to use the full dataset (you need need to upload it first of course)
BUCKET_TRAIN_DATA_PATH = 'data/png'

##### Training  - - - - - - - - - - - - - - - - - - - - - -

IMG_SIZE = 256
BATCH_SIZE = 16

##### Model - - - - - - - - - - - - - - - - - - - - - - - -

# model folder name (will contain the folders for all trained model versions)
MODEL_NAME = 'class_model'

# model version folder name (where the trained model.joblib file will be stored)


### GCP AI Platform - - - - - - - - - - - - - - - - - - - -

# not required here
