# tests/unit/utils/test_file_utils.py

import os
import tempfile
from app.utils.file_utils import (
    ensure_directories,
    generate_temp_filename,
    save_file,
    read_file
)

def test_ensure_directories_creates_folder(tmp_path):
    test_dir = tmp_path / "new_folder"
    assert not test_dir.exists()

    ensure_directories(str(test_dir))

    assert test_dir.exists()
    assert test_dir.is_dir()

def test_generate_temp_filename_default_extension():
    filename = generate_temp_filename()
    assert filename.endswith(".xml")
    assert len(filename.replace(".xml", "")) == 32  # UUID hex length

def test_generate_temp_filename_custom_extension():
    filename = generate_temp_filename(".txt")
    assert filename.endswith(".txt")

def test_save_and_read_file_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.xml")
        content = b"<xml>Testinhalt</xml>"

        save_file(content, path)
        result = read_file(path)

        assert result == content
