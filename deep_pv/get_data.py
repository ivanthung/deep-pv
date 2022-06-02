#package import
from google.cloud import storage

from deep_pv.params import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH, IMG_SIZE, BATCH_SIZE


#functions to import data

#get image for prediction from GCP
#saved locally as "file_name.png"
def get_predict_image_gcp(file_name):
    """method to get the training data (or a portion of it) from google cloud bucket"""
    # Add Client() here
    client = storage.Client()
    path = f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}/{file_name}.png"
    #prepare data into train and test sets
    bucket = client.bucket(BUCKET_NAME)
    print(bucket)
    blob = bucket.blob(f'{BUCKET_TRAIN_DATA_PATH}/{file_name}.png')
    blob.download_to_filename('{file_name}.png')
    return '{file_name}.png'

    #return train_ds, test_ds
if __name__ =="__main__":
    get_predict_image_gcp()
