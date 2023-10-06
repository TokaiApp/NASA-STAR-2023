import os
from azure.storage.blob import BlobServiceClient

from dotenv import load_dotenv

load_dotenv()
# Retrieve the connection string for use with the application. The storage
# connection string is stored in an environment variable on the machine
# running the application called AZURE_STORAGE_CONNECTION_STRING. If the environment variable is
# created after the application is launched in a console or with Visual Studio,
# the shell or application needs to be closed and reloaded to take the
# environment variable into account.
connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

class BlobStorage:
    def __init__(self):
        # Create the BlobServiceClient object
        self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    def upload_blob(self, file, file_name, user_email):
        """
        Upload a blob to a given container
        """
        container_name = "user-knowledge-base"
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_name)
        result = blob_client.upload_blob(data=file, metadata={"file_name": file_name, "user_email": user_email}, 
                                         overwrite=True)
        
        if result:
            return True
        else:
            print("Error uploading blob")
            return False