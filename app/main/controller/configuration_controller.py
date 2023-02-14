from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from ..service.configuration_service import get_configuration, create_or_update_configuration
from ..util.configuration_dto import ConfigurationDto

api = ConfigurationDto.api


@api.route("/")
@api.response(404, "Configuration Not Found")
class Configuration(Resource):
    def get(self):
        """get configuration"""
        return get_configuration()

    @api.response(200, "Configuration successfully Updated.")
    def post(self) -> Tuple[Dict[str, str], int]:
        """Create/Update configuration"""
        data = request.json
        return create_or_update_configuration(data=data)
