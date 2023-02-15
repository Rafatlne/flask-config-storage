from marshmallow import Schema, fields
from flask_restx import Namespace


class ConfigurationSchema(Schema):
    firstName = fields.Str(required=True)
    secondName = fields.Str(required=True)
    ageInYears = fields.Integer(required=True, strict=True)
    address = fields.Str(required=True)
    creditScore = fields.Float(required=True)


class ConfigurationDto:
    api = Namespace("config", description="configuration related operations")
