from typing import Dict, Tuple

from flask import request
from flask_restx import Resource
from flask.typing import ResponseReturnValue

from ..service.configuration_service import ConfigurationService
from ..util.configuration_dto import ConfigurationDto

api = ConfigurationDto.api


@api.route("/")
class Configuration(Resource):
    configuration_service = ConfigurationService()

    def get(self) -> ResponseReturnValue:
        """get configuration"""
        return self.configuration_service.get_configuration()

    def post(self) -> ResponseReturnValue:
        """Create/Update configuration"""
        data = request.json
        return self.configuration_service.create_or_update_configuration(data=data)

