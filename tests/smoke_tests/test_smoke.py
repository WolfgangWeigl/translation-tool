import pytest

@pytest.mark.smoke
def test_server_is_running(client):
    response = client.get("/")
    assert response.status_code == 200
