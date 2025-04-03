# tests/integration/routes/test_guide.py

import pytest

@pytest.mark.integration
def test_guide_route(client):
    # Teste den Zugriff auf die /guide-Seite
    response = client.get("/guide")
    assert response.status_code == 200

    html = response.data.decode("utf-8")

    # Überprüfen der Grundstruktur
    assert "<html" in html
    assert "<main" in html
    assert "<h1" in html
    assert "Guide" in html

    # Sicherstellen, dass der Inhalt von guide.html angezeigt wird
    assert "How to Use the Translation Tool" in html
    assert "This guide provides a step-by-step explanation of the application's main workflow and features." in html
    assert "Step 1: Starting from the Home Page" in html
    assert "Step 2: Upload and Configure Translation" in html
    assert "Step 3: Translation Progress and Download" in html
    assert "Step 4: Using the Editor" in html

    # Sicherstellen, dass der Accordion-Teil des Inhalts korrekt geladen wird
    assert "accordion" in html
    assert "Step 1" in html
    assert "Step 2" in html
    assert "Step 3" in html
    assert "Step 4" in html

    # Überprüfen, ob Modal- und Bild-Links vorhanden sind
    assert 'data-bs-target="#modalImageStep1"' in html
    assert 'data-bs-target="#modalImageStep2"' in html
    assert 'data-bs-target="#modalImageStep3"' in html
    assert 'data-bs-target="#modalImageStep4"' in html

    # Sicherstellen, dass auch das Troubleshooting und die Feedback-Sektion vorhanden sind
    assert "Common Issues & Troubleshooting" in html
    assert "Feel stuck or have improvement ideas?" in html
    assert "project repository" in html
