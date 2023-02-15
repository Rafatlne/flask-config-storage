import json

from app.main.service import storage_service as storage_service_module


class TestConfigurationController:
    def test_get_config_request_will_give_200(self, mocker, api_test_client):
        validated_config_json_data = {
            "firstName": "Foo",
            "secondName": "Foo",
            "address": "Foo",
            "ageInYears": 1,
            "creditScore": 1.1,
        }

        def get_config_file_in_byte():
            return b'{"firstName": "Foo","secondName": "Foo","address": "Foo","ageInYears": 1,"creditScore": 1.1}'

        mocker.patch("google.cloud.storage.Client")
        mocker.patch(
            "google.cloud.storage.Blob.download_as_string",
            side_effect=get_config_file_in_byte,
        )
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False

        response = api_test_client.get("/config/")
        data = response.json

        assert data == validated_config_json_data

    def test_if_config_file_does_not_exists_it_will_give_404_status_code(
        self, mocker, api_test_client
    ):
        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Blob.exists", return_value=False)
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False

        response = api_test_client.get("/config/")
        status_code = response.status_code

        assert status_code == 404

    def test_invalid_json_schema_post_request_will_give_400_status(
        self, mocker, api_test_client
    ):
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

        response = api_test_client.post(
            "/config/",
            data=json.dumps(invalid_config_json_data),
            content_type="application/json",
        )
        status_code = response.status_code

        assert status_code == 400

    def test_valid_json_schema_post_request_will_give_200_status(
        self, mocker, api_test_client
    ):
        validated_config_json_data = {
            "firstName": "Foo",
            "secondName": "Foo",
            "address": "Foo",
            "ageInYears": 1,
            "creditScore": 1.1,
        }

        mocker.patch("google.cloud.storage.Client")
        mocker.patch("google.cloud.storage.Bucket")
        mocker.patch("google.cloud.storage.Blob")
        storage_service_module._path_to_private_key = "path/to/private/key.json"
        storage_service_module._emulate_gcs_server = False

        response = api_test_client.post(
            "/config/",
            data=json.dumps(validated_config_json_data),
            content_type="application/json",
        )
        status_code = response.status_code

        assert status_code == 200
