from flask_restx import Namespace


class HealthCheckDto:
    """Data Transfer object for health check"""
    api = Namespace("health-check", description="health check api")
