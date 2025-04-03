import pytest

@pytest.mark.integration
def test_get_diff_data(client, monkeypatch):
    # Simuliertes temp_data mit Byte-Strings
    class FakeTempData(dict):
        def get(self, key):
            return {
                "original": b"<xml>original</xml>",
                "translation": b"<xml>translated</xml>"
            }.get(key, None)

    # temp_data in socket_events ersetzen
    monkeypatch.setattr("app.socket_events.temp_data", FakeTempData())

    response = client.get("/get_diff_data")
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["original"] == "<xml>original</xml>"
    assert json_data["translation"] == "<xml>translated</xml>"


@pytest.mark.integration
def test_get_diff_data_missing_keys(client, monkeypatch):
    monkeypatch.setattr("app.socket_events.temp_data", {})

    response = client.get("/get_diff_data")
    assert response.status_code == 200
    data = response.get_json()
    assert data["original"] is None
    assert data["translation"] is None
