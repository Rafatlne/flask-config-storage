from marshmallow import Schema, fields
from flask_restx import Namespace


class Configuration:
    def __init__(self, firstName, secondName, ageInYears, address, creditScore):
        self.firstName = firstName
        self.secondName = secondName
        self.ageInYears = ageInYears
        self.address = address
        self.creditScore = creditScore

    def __repr__(self):
        return f"<Configuration(name={self.firstName + self.secondName!r})>"


class ConfigurationSchema(Schema):
    firstName = fields.Str(required=True)
    secondName = fields.Str(required=True)
    ageInYears = fields.Integer(required=True, strict=True)
    address = fields.Str(required=True)
    creditScore = fields.Float(required=True)


class ConfigurationDto:
    api = Namespace("config", description="configuration related operations")
