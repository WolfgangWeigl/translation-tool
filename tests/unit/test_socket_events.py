# tests/unit/test_socket_events.py

import pytest
from flask import Flask
import app.socket_events as se  # wichtig für korrektes Patching

# DummySocket zum Abfangen von socketio.emit-Aufrufen
class DummySocket:
    def __init__(self):
        self.emits = []

    def emit(self, event, data):
        self.emits.append((event, data))


# Flask-App-Kontext für Tests
@pytest.fixture
def app_context():
    app = Flask("test_socket_events")
    app.config["LT_URL"] = "http://dummy-url"
    with app.app_context():
        yield app


# DummySocket für monkeypatch
@pytest.fixture
def dummy_socket(monkeypatch):
    dummy = DummySocket()
    monkeypatch.setattr(se, "socketio", dummy)
    return dummy


# Fixture zum Zurücksetzen von temp_data vor jedem Test
@pytest.fixture(autouse=True)
def reset_temp_data():
    se.temp_data.clear()
    yield
    se.temp_data.clear()


# Test: Erfolgreicher Upload und Verarbeitung eines XML-Files
def test_handle_upload_xml_success(app_context, dummy_socket, monkeypatch):
    fake_result = {
        "original": b"<xml>original</xml>",
        "translation": b"<xml>translated</xml>",
        "merged": b"<xml>merged</xml>",
        "progress": 100
    }

    monkeypatch.setattr(se, "process_xml_translation", lambda data, socketio=None: fake_result)

    dummy_data = {
        "fileName": "test.xml",
        "fileType": "XML",
        "fileData": b"<xml>original</xml>",
        "srcLang": "en",
        "destLang": "de",
        "transType": "single"
    }

    se.handle_upload(dummy_data)

    assert se.temp_data["original"] == b"<xml>original</xml>"
    assert se.temp_data["translation"] == b"<xml>translated</xml>"
    assert se.temp_data["merged"] == b"<xml>merged</xml>"

    events = [event for event, _ in dummy_socket.emits]
    assert "upload_progress" in events
    assert "translation_progress" in events

def test_handle_upload_xml_raises_exception(app_context, dummy_socket, monkeypatch):
    # Mock wirft absichtlich einen Fehler
    def fail_translation(*args, **kwargs):
        raise Exception("something went wrong")

    monkeypatch.setattr(se, "process_xml_translation", fail_translation)

    dummy_data = {
        "fileName": "test.xml",
        "fileType": "XML",
        "fileData": b"<xml>original</xml>",
        "srcLang": "en",
        "destLang": "de",
        "transType": "single"
    }

    se.handle_upload(dummy_data)

    # Fehler wurde per socketio gesendet
    errors = [data.get("message", "") for event, data in dummy_socket.emits if event == "error"]
    assert any("XML Translation Error" in msg for msg in errors)

# Test: Upload eines MBZ-Files
def test_handle_upload_mbz_file(app_context, dummy_socket):
    dummy_data = {
        "fileName": "test.mbz",
        "fileType": "MBZ",
        "fileData": b"fake",
        "srcLang": "en",
        "destLang": "de",
        "transType": "single"
    }

    se.handle_upload(dummy_data)

    logs = [data.get("message", "") for event, data in dummy_socket.emits if event == "log"]
    assert any("MBZ-Dateien" in msg for msg in logs)


# Test: Upload eines unbekannten Dateityps
def test_handle_upload_unknown_type(app_context, dummy_socket):
    dummy_data = {
        "fileName": "test.unknown",
        "fileType": "XYZ",
        "fileData": b"???",
        "srcLang": "en",
        "destLang": "de",
        "transType": "single"
    }

    se.handle_upload(dummy_data)

    errors = [data.get("message", "") for event, data in dummy_socket.emits if event == "error"]
    assert any("Unbekannter Dateityp" in msg for msg in errors)
