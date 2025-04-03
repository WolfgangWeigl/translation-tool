import pytest
from app.app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    return flask_app.test_client()
