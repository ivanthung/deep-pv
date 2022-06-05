from google.cloud import storage
from deep_pv.params import PATH_TO_LOCAL_MODEL, BUCKET_NAME

def download_blob_into_memory(bucket_name, blob_name):
    """Downloads a blob into memory."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(blob_name)
    contents = blob.download_as_string()

    print(
        "Downloaded storage object {} from bucket {} as the following string: {}.".format(
            blob_name, bucket_name, contents
        )
    )

def get_blob_list():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(PATH_TO_LOCAL_MODEL)
    for blob in blobs:
        print(blob)


if __name__ == '__main__':
    get_blob_list()
