import json
import os
from typing import Dict, Any

from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
from werkzeug.exceptions import BadRequest, NotFound

_path_to_private_key = os.getenv("PATH_TO_GCS_PRIVATE_KEY", None)
_bucket_name = os.getenv("BUCKET_NAME", "stored-configuration-files")
_emulate_gcs_server = os.getenv("EMULATE_GCS_SERVER", "False") == "True"


class StorageService:
    """This Class handles Google Storage Service related operation"""

    gcs_client = None
    storage_bucket_object = None

    def __init__(self) -> None:
        self._set_client()
        self._check_bucket_exists()

    def _set_client(self) -> None:
        self.gcs_client = (
            self.get_emulated_gcs_client()
            if _emulate_gcs_server
            else self.get_gcs_client()
        )
        self.storage_bucket_object = storage.Bucket(self.gcs_client, _bucket_name)

    @staticmethod
    def get_emulated_gcs_client() -> storage.Client:
        """Get emulated google storage client

        :return:
        """
        emulated_gcs_client = storage.Client(
            client_options={
                "api_endpoint": os.getenv(
                    "EMULATED_GCS_SERVER_ENDPOINT", "http://localhost:4443"
                )
            },
            credentials=AnonymousCredentials(),
            project="test",
        )
        return emulated_gcs_client

    @staticmethod
    def get_gcs_client() -> storage.Client:
        """Get Google Storage Client

        checks google service authentication json file exists

        :return: google storage client object
        :raise 400: if google service authentication json file doesn't exist
        """
        if not _path_to_private_key:
            raise BadRequest("Please Properly Setup Google Cloud Storage!")

        gcs_client = storage.Client.from_service_account_json(
            json_credentials_path=_path_to_private_key
        )

        return gcs_client

    def _check_bucket_exists(self) -> None:
        """Checks Google storage bucket exists

        :raise 404: if google storage bucket doesn't exist
        """
        if not self.storage_bucket_object.exists():
            raise NotFound("GCS bucket doesn't exists!")

    def _check_file_exists(self, file_name: str) -> bool:
        """Get Boolean value if file exists or not in google bucket

        checks blob file exists or not
        :param file_name: that will be searched in google bucket
        :return: True/False
        """
        file_blob = self.storage_bucket_object.blob(file_name)

        return file_blob.exists()

    def get_config_file(self, file_name: str = "configuration-file.json") -> storage.Blob:
        """Get File Blob from Google Storage

        checks file exists or not
        :param file_name: that will be searched in google bucket
        :return: Blob object from Google Bucket
        :raise 404: if file doesn't exist
        """
        if not self._check_file_exists(file_name):
            raise NotFound("Config file doesn't exists!")

        blob = self.storage_bucket_object.blob(file_name)

        return blob

    def upload_config_file(
        self, json_file_data: Dict[str, Any], file_name: str = "configuration-file.json"
    ) -> None:
        """Create and Delete file blob in Google Storage
        checks if file exist

        :param json_file_data: payload of json data of post request that will be uploaded on Google storage
        :param file_name: file name for blob
        """
        if self._check_file_exists(file_name):
            blob = self.get_config_file()
            blob.delete()
        file_blob = self.storage_bucket_object.blob(file_name)
        file_blob.upload_from_string(
            json.dumps(json_file_data), content_type="application/json"
        )
