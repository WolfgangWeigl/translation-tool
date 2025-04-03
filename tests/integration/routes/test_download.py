import pytest

@pytest.mark.integration
def test_download_single_translation(client, monkeypatch):
    # Temp-Daten für einfachen Einzel-Download
    fake_translation = b"<xml>translated</xml>"

    monkeypatch.setattr("app.socket_events.temp_data", {
        "transType": "single",
        "translation": fake_translation
    })

    response = client.get("/download")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "<xml>translated</xml>"


@pytest.mark.integration
def test_download_multiple_translation(client, monkeypatch):
    # Temp-Daten für "multiple" Mode → merged wird benutzt
    fake_merged = b"<xml>merged version</xml>"

    monkeypatch.setattr("app.socket_events.temp_data", {
        "transType": "multiple",
        "merged": fake_merged
    })

    response = client.get("/download")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "<xml>merged version</xml>"
