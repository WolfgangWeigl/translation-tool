# tests/unit/translation/test_libretranslate_api.py

import pytest
import requests
from app.translation.libretranslate_api import translate_text

@pytest.mark.unit
def test_translate_text_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"translatedText": "Hallo Welt"}
    mock_response.raise_for_status = mocker.Mock()
    
    mocker.patch("requests.post", return_value=mock_response)

    result = translate_text("http://dummy-url/translate", "Hello world", "en", "de")

    assert result == "Hallo Welt"
    requests.post.assert_called_once_with(
        "http://dummy-url/translate",
        data={
            "q": "Hello world",
            "source": "en",
            "target": "de",
            "format": "html"
        }
    )

@pytest.mark.unit
def test_translate_text_error_returns_original(mocker):
    mocker.patch("requests.post", side_effect=requests.RequestException("Server down"))

    result = translate_text("http://dummy-url/translate", "Hello world", "en", "de")

    assert result == "Hello world"
