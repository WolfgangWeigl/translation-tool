# tests/integration/routes/test_mbz.py
 
import pytest

@pytest.mark.integration
def test_mbz_route(client):
    response = client.get("/mbz")
    assert response.status_code == 200

    html = response.data.decode("utf-8")

    # Struktur
    assert "<html" in html
    assert "<form" in html
    assert "upload-form" in html

    # Sprachfelder
    assert "originalLanguage" in html
    assert "targetLanguage" in html

    # Buttons
    assert "translateBtn" in html
    assert "editorBtn" in html
    assert "downloadBtn" in html

