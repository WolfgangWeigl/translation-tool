import pytest
import libretranslatepy  # <- wichtig!

@pytest.mark.integration
def test_xml_route_with_mocked_languages(client, monkeypatch):
    # Simulierter API-Client
    class MockLT:
        def languages(self):
            return [
                {"code": "en", "name": "English"},
                {"code": "de", "name": "German"}
            ]

    # Patch die Klasse direkt im Original-Modul
    monkeypatch.setattr(libretranslatepy, "LibreTranslateAPI", lambda _: MockLT())

    response = client.get("/xml")
    assert response.status_code == 200

    html = response.data.decode("utf-8")
    assert "English" in html
    assert "German" in html
    assert "form.js" in html
    assert "socket.js" in html
