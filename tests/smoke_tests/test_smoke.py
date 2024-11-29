import requests

def test_app_is_running():
    response = requests.get("http://localhost:80")
    assert response.status_code == 200