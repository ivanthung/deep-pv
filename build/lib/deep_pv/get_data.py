from google.cloud import storage
from deep_pv.params import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH, WEIGHTS_PATH
from PIL import Image
from io import BytesIO
import numpy as np
import os

def get_predict_image_gcp(file_name, image_type = 'jpg'):
    """Method to get one training file from google cloud bucket"""

    client = storage.Client()
    blob_path = f'{BUCKET_TRAIN_DATA_PATH}/{file_name}.{image_type}'
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_path)
    data = blob.download_as_string()
    im = Image.open(BytesIO(data))
    return np.asarray(im)

def download_weights():
    """ Proof of concept to download the weights from GCP.
    TODO:
    - list all available h5 files on the server.
    - check if that file exists in the trained_weights file.
    - if it doesn't, download that file to the folder/
    """

    prefix = 'train_data/trained_weights/'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

    download_name = blob.name.split("/")[-1]
    if not (os.path.exists(WEIGHTS_PATH + download_name)):
        print("Fetching latest weights from GCP...")
        blob.download_to_filename(WEIGHTS_PATH + download_name)
    else:
        print("Latest weights available locally: ", download_name)

    return (WEIGHTS_PATH + download_name)

if __name__ =="__main__":

    print(download_weights())
    # # Load and print image
    # loaded_im = get_predict_image_gcp('51.906771_4.451552')
    # plt.imshow(loaded_im)
    # plt.show()
