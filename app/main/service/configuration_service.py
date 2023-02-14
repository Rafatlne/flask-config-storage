from marshmallow import ValidationError

from app.main.util.configuration_dto import Configuration, ConfigurationSchema


def get_configuration():
    configuration = Configuration(
        firstName="Monty", secondName="Rafat", ageInYears="1", address="dhaka", creditScore=12.99
    )
    configuration_schema = ConfigurationSchema()
    result = configuration_schema.dump(configuration)

    return result


def create_or_update_configuration(data):
    try:
        configuration_schema = ConfigurationSchema()
        result = ConfigurationSchema().load(data)
    except ValidationError as err:
        return err.messages, 400
