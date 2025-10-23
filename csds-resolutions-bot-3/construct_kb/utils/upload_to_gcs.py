"""Functions to upload JSON files to Google Cloud Storage (GCS)."""

from google.cloud import storage


def upload_json_file_to_gcs(
    project_id: str,
    bucket_name: str,
    source_file_path: str,
    destination_blob_name: str,
):
    """Uploads a JSON file to the GCS bucket.

    Args:
        project_id (str): The ID of your Google Cloud project.
        bucket_name (str): The ID of your GCS bucket.
        source_file_path (str): The path to your local JSON file.
        destination_blob_name (str): The path/name of the object in GCS.
    """
    try:
        # Initialize a client
        client = storage.Client(project=project_id)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Set the content type explicitly to application/json
        # This helps browsers/applications correctly interpret the file upon
        # download.
        blob.content_type = 'application/json'

        # Upload the file
        blob.upload_from_filename(source_file_path)

        print(
            f"File '{source_file_path}' uploaded \
            to '{destination_blob_name}'\
            in bucket '{bucket_name}'."
        )
        print(f'Public URL: gs://{bucket_name}/{destination_blob_name}')

    except FileNotFoundError:
        print(f"Error: The local file '{source_file_path}' was not found.")
    except Exception as e:
        print(f'An error occurred during file upload: {e}')
