import pytest
from app.utils.progress import emit_progress
from unittest.mock import MagicMock

@pytest.mark.unit
def test_emit_progress_emits_correct_data():
    mock_socketio = MagicMock()
    emit_progress(mock_socketio, current=50, total=100)
    mock_socketio.emit.assert_called_once_with(
        'translation_progress',
        {'progress': 50.0, 'finished': False}
    )

@pytest.mark.unit
def test_emit_progress_handles_zero_total():
    mock_socketio = MagicMock()
    emit_progress(mock_socketio, current=50, total=0)
    mock_socketio.emit.assert_not_called()

@pytest.mark.unit
def test_emit_progress_handles_missing_socketio():
    emit_progress(None, current=50, total=100)
