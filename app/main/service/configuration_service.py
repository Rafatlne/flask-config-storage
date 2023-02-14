import json

from marshmallow import ValidationError

from app.main.service.storage_service import StorageService
from app.main.util.configuration_dto import ConfigurationSchema


class ConfigurationService:

    def get_configuration(self):
        storage_service = StorageService()
        config_file_blog = storage_service.get_config_file()
        byte_config_file_str_content = config_file_blog.download_as_string()
        config_file_str_content = byte_config_file_str_content.decode("utf-8")
        configuration_schema = ConfigurationSchema()
        configuration_json_data = configuration_schema.dump(
            json.loads(config_file_str_content)
        )

        return configuration_json_data

    def create_or_update_configuration(self, data):
        storage_service = StorageService()
        try:
            configuration_schema = ConfigurationSchema()
            configuration_json_data = configuration_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        storage_service.upload_config_file(configuration_json_data)
        return {"message": "Configuration successfully Updated."}, 200
