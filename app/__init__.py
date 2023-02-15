from flask_restx import Api
from flask import Blueprint

from .main.controller.configuration_controller import api as configuration_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='FLASK CONFIG STORAGE',
    version='1.0',
    description='a boilerplate for flask restplus (restx) web service',
    authorizations=authorizations,
    security='apikey',
    doc=False
)

api.add_namespace(configuration_ns)
