import pytest
from flask import Flask

# Einfaches Flask App für Tests
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/')
    def hello():
        return "Hello, World!"
    
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Beispiel für einen Test
def test_hello(client):
    response = client.get('/')
    assert response.data == b"Hello, World!"
    assert response.status_code == 200
