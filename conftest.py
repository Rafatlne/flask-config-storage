import pytest

from app import blueprint
from app.main import create_app


@pytest.fixture(scope='module')
def api_test_client():
    app = create_app('test')
    app.register_blueprint(blueprint)

    app.app_context().push()
    with app.test_client() as testing_client:
        yield testing_client
