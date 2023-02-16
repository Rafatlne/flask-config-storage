import json
from typing import Any, Dict, Tuple

from marshmallow import ValidationError

from app.main.service.storage_service import StorageService
from app.main.util.configuration_dto import ConfigurationSchema


class ConfigurationService:
    """This Class handles get,create, update related operation for configuration-file.json file"""

    def get_configuration(self) -> Dict[str, Any]:
        """Get a data of configuration-file.json

        :return: data as json format of configuration-file.json
        :raise 404: if configuration-file.json doesn't exist
        :raise 404: if Google storage bucket doesn't exist
        :raise 404: if json authentication account key for Google storage doesn't exist
        """
        storage_service = StorageService()
        config_file_blog = storage_service.get_config_file()
        byte_config_file_str_content = config_file_blog.download_as_string()
        config_file_str_content = byte_config_file_str_content.decode("utf-8")
        configuration_schema = ConfigurationSchema()
        configuration_json_data = configuration_schema.dump(
            json.loads(config_file_str_content)
        )

        return configuration_json_data

    def create_or_update_configuration(
        self, data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], int]:
        """Create or Update data of configuration-file.json

        checks json data from post request is matched with provided json schema

        :param data: payload from post request
        :return: successful json data
        :raise 404: if Google storage bucket doesn't exist
        :raise 404: if json authentication account key for Google storage doesn't exist
        :raise 400: if data is not valid json schema
        """
        storage_service = StorageService()
        try:
            configuration_schema = ConfigurationSchema()
            configuration_json_data = configuration_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        storage_service.upload_config_file(configuration_json_data)
        return {"message": "Configuration successfully Updated."}, 200
