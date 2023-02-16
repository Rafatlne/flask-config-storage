from flask_restx import Api
from flask import Blueprint

from .main.controller.configuration_controller import api as configuration_ns

blueprint = Blueprint("api", __name__)


@blueprint.route("/")
def health_check():
    return {"message": "Application heath is ok."}, 200


authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    blueprint,
    title="FLASK CONFIG STORAGE",
    version="1.0",
    description="a flask google storage connection api",
    authorizations=authorizations,
    security="apikey",
    doc="/doc/",
)

api.add_namespace(configuration_ns)
