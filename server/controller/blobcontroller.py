from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from typing import List


# from io import BytesIO

# def upload_to_azure_blob(file_path, blob_configs, blob_name):
def upload_to_azure_blob(file_name, blob_configs):
    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(blob_configs[0])

    # Create a ContainerClient
    container_client = blob_service_client.get_container_client(blob_configs[1])

    # Upload the file
    with open(file_name, "rb") as data:
        container_client.upload_blob(name=file_name, data=data)


def get_from_azure_blob(blob_name: str, blob_configs: List[str]):
    blob_service_client = BlobServiceClient.from_connection_string(blob_configs[0])

    # Create a ContainerClient
    container_client = blob_service_client.get_container_client(blob_configs[1])

    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob()

    return blob_data


