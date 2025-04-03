import pytest

@pytest.mark.integration
def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200  # neu: Statuscode prüfen
    html = response.data.decode("utf-8")
    
    # Grundstruktur
    assert "<html" in html
    assert "What do you want to translate?" in html
    
    # Verlinkungen prüfen
    assert "/xml" in html
    assert "MBZ File" in html
    assert "XML File" in html

    # Badge-Markierungen (Bonus)
    assert "badge rounded-pill bg-dark" in html
    assert "badge rounded-pill bg-success" in html

