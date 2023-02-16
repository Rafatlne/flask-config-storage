import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Config"""
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False


class DevelopmentConfig(Config):
    """Dev config for localhost"""
    DEBUG = True


class TestingConfig(Config):
    """Test config for testing"""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Config for production"""
    DEBUG = False


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)

key = Config.SECRET_KEY
