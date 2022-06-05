# def download_model(BUCKET_NAME):
#     prefix = 'models/mrcnn/'
#     dl_dir = 'mrcnn/'
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(BUCKET_NAME)
#     blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
#     for blob in blobs:
#         if blob.name.endswith("/"):
#             continue
#         file_split = blob.name.split("/")
#         directory = "/".join(file_split[0:-1])
#         Path(directory).mkdir(parents=True, exist_ok=True)
#         blob.download_to_filename(blob.name)

def get_model_weights():
        # Add Client() here
    client = storage.Client()
    path = f"gs://{BUCKET_NAME}/models/model_weights_path.h5"
    #prepare data into train and test sets
    bucket = client.bucket(BUCKET_NAME)
    print(bucket)
    blob = bucket.blob(f'models/model_weights_path.h5')
    blob.download_to_filename('models/model_weights_path.h5')
