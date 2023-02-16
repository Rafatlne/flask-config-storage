import json

import pytest
from werkzeug.exceptions import BadRequest, NotFound

from app.main.service.configuration_service import ConfigurationService
from app.main.service.storage_service import StorageService
from app.main.service import storage_service as storage_service_module


class TestStorageService:
    def test_emulated_gcs_client_will_give_404_if_bucket_doesnt_exists(self, mocker):
        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Bucket.exists", return_value=False)
        storage_service_module._emulate_gcs_server = True
        with pytest.raises(NotFound):
            StorageService()

    def test_emulated_gcs_client_will_give_404_if_config_json_file_does_not_exist_it_will_give_404_request(
        self, mocker
    ):
        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Blob.exists", return_value=False)
        storage_service_module._emulate_gcs_server = True
        storage_service = StorageService()
        with pytest.raises(NotFound):
            config_json_file = storage_service.get_config_file()

    def test_if_path_of_private_key_not_given_it_will_throw_400_status(self, mocker):
        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Bucket.exists", return_value=True)
        storage_service_module._path_to_private_key = None
        storage_service_module._emulate_gcs_server = False
        with pytest.raises(BadRequest):
            StorageService()

    def test_if_bucket_name_does_not_exist_it_will_give_404_request(self, mocker):
        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Bucket.exists", return_value=False)
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False
        with pytest.raises(NotFound):
            StorageService()

    def test_if_config_json_file_does_not_exist_it_will_give_404_request(self, mocker):
        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Blob.exists", return_value=False)
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False
        storage_service = StorageService()
        with pytest.raises(NotFound):
            config_json_file = storage_service.get_config_file()

    def test_get_config_file_from_gcs(self, mocker):
        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Blob")
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False
        storage_service = StorageService()
        config_json_file = storage_service.get_config_file()

        assert config_json_file.exists()

    def test_upload_config_data_as_json_in_gcs(self, mocker):
        validated_config_json_data = {
            "firstName": "Foo",
            "secondName": "Foo",
            "address": "Foo",
            "ageInYears": 1,
            "creditScore": 1.1,
        }

        def get_config_file_in_byte():
            return b'[{"firstName": "Foo","secondName": "Foo","address": "Foo","ageInYears": 1,"creditScore": 1.1}]'

        def get_config_json_data(key):
            return {
                "firstName": "Foo",
                "secondName": "Foo",
                "address": "Foo",
                "ageInYears": 1,
                "creditScore": 1.1,
            }

        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Bucket")
        mocker.patch(
            "google.cloud.storage.Blob.download_as_string",
            side_effect=get_config_file_in_byte,
        )
        mocker.patch("json.loads", side_effect=get_config_json_data)
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False
        storage_service = StorageService()
        storage_service.upload_config_file(validated_config_json_data)


class TestConfigurationService:
    def test_get_configuration(self, mocker):
        validated_config_json_data = {
            "firstName": "Foo",
            "secondName": "Foo",
            "address": "Foo",
            "ageInYears": 1,
            "creditScore": 1.1,
        }

        def get_config_file_in_byte():
            return b'[{"firstName": "Foo","secondName": "Foo","address": "Foo","ageInYears": 1,"creditScore": 1.1}]'

        mocker.patch("google.cloud.storage.Client")
        mocker.patch(
            "google.cloud.storage.Blob.download_as_string",
            side_effect=get_config_file_in_byte,
        )
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False
        configuration_service = ConfigurationService()
        config_json_data = configuration_service.get_configuration()

        assert config_json_data == [validated_config_json_data]

    def test_invalid_json_schema_will_throw_400_status(self, mocker):
        invalid_config_json_data = {
            "firstName": 1,
            "secondName": 1,
            "address": 1,
            "ageInYears": "bar",
            "creditScore": "bar",
        }
        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Bucket")
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False
        configuration_service = ConfigurationService()
        response, status = configuration_service.create_or_update_configuration(
            invalid_config_json_data
        )

        assert status == 400

    def test_valid_json_config_data_will_upload_gcs_server(self, mocker):
        validated_config_json_data = {
            "firstName": "Foo",
            "secondName": "Foo",
            "address": "Foo",
            "ageInYears": 1,
            "creditScore": 1.1,
        }

        def get_config_file_in_byte():
            return b'[{"firstName": "Foo","secondName": "Foo","address": "Foo","ageInYears": 1,"creditScore": 1.1}]'

        def get_config_json_data(key):
            return {
                "firstName": "Foo",
                "secondName": "Foo",
                "address": "Foo",
                "ageInYears": 1,
                "creditScore": 1.1,
            }

        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Bucket")
        mocker.patch(
            "google.cloud.storage.Blob.download_as_string",
            side_effect=get_config_file_in_byte,
        )
        mocker.patch("json.loads", side_effect=get_config_json_data)
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False
        configuration_service = ConfigurationService()
        response, status = configuration_service.create_or_update_configuration(
            validated_config_json_data
        )

        assert status == 200
