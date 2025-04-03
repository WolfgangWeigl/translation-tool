import pytest

@pytest.mark.integration
def test_editor_route(client):
    response = client.get("/editor")
    assert response.status_code == 200

    html = response.data.decode("utf-8")

    # Grundstruktur: HTML & Editor-Div
    assert "<html" in html
    assert 'id="editor"' in html
    assert "height: 90vh" in html

    # Buttons im Footer
    assert 'id="resetBtn"' in html
    assert 'id=\'downloadBtn\'' in html
    assert "/download" in html

    # Javascript eingebunden?
    assert "editor.js" in html
