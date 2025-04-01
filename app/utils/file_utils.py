# utils/file_utils.py

import os
import uuid

def ensure_directories(*dirs):
    """
    Erstellt alle angegebenen Ordner (falls nicht vorhanden).
    """
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

def generate_temp_filename(extension=".xml"):
    """
    Generiert zufälligen Dateinamen mit angehängter Endung.
    """
    return f"{uuid.uuid4().hex}{extension}"

def save_file(file_data, path):
    """
    Speichert binäre Daten an einem Pfad.
    """
    with open(path, "wb") as f:
        f.write(file_data)

def read_file(path):
    with open(path, "rb") as f:
        return f.read()
