import json
import os

from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
from werkzeug.exceptions import BadRequest

_path_to_private_key = os.getenv("PATH_TO_GCS_PRIVATE_KEY", None)
_bucket_name = os.getenv("BUCKET_NAME", "stored-configuration-files")
_emulate_gcs_server = os.getenv("EMULATE_GCS_SERVER", "False") == "True"


class StorageService:
    gcs_client = None
    storage_bucket_object = None

    def __init__(self):
        self._set_client()
        self._check_bucket_exists()

    def _set_client(self):
        self.gcs_client = (
            self.get_emulated_gcs_client() if _emulate_gcs_server else self.get_gcs_client()
        )
        self.storage_bucket_object = storage.Bucket(self.gcs_client, _bucket_name)

    @staticmethod
    def get_emulated_gcs_client():
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
    def get_gcs_client():
        gcs_client = storage.Client.from_service_account_json(
            json_credentials_path=_path_to_private_key
        )

        return gcs_client

    def _check_bucket_exists(self):
        if not self.storage_bucket_object.exists():
            raise BadRequest("GCS bucket doesn't exists!")

    def _check_file_exists(self, file_name):
        file_blob = self.storage_bucket_object.blob(file_name)

        return file_blob.exists()

    def get_config_file(self, file_name="configuration-file.json"):
        if not self._check_file_exists(file_name):
            raise BadRequest("Config file doesn't exists!")

        blob = self.storage_bucket_object.blob(file_name)

        return blob

    def upload_config_file(self, json_file_data, file_name="configuration-file.json"):
        blob = self.storage_bucket_object.blob(file_name)

        if self._check_file_exists(file_name):
            blob = self.get_config_file()
            blob.delete()

        blob.upload_from_string(
            json.dumps(json_file_data), content_type="application/json"
        )
