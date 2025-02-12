import os
import secrets
import requests

from extractor import extract_mbz
from translator import translate_mbz
from xml_translator import translate_xml

from libretranslatepy import LibreTranslateAPI

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['EXTRACTION_FOLDER'] = os.getenv('EXTRACTION_FOLDER')
app.config['TRANSLATION_FOLDER'] = os.getenv('TRANSLATION_FOLDER')
app.config['MAX_HTTP_BUFFER_SIZE'] = int(os.getenv('MAX_HTTP_BUFFER_SIZE'))
app.config['LT_URL'] = os.getenv('LT_URL')

# Flask-SocketIO für WebSocket-Kommunikation, hier mit erhöhter Puffergröße
socketio = SocketIO(app, 
                    max_http_buffer_size=int(app.config['MAX_HTTP_BUFFER_SIZE']), 
                    logger=True, 
                    enginio_logger=True)

# Speichert temporär die Form-Daten
temp_data = {}

# Hauptseite
@app.route('/')
def index():
    try:
        requests.get(app.config['LT_URL'], timeout=10)
        return render_template('index.html')
    
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {type(e).__name__}")
        return render_template('error.html', error={"type": type(e).__name__, "description": e})
    
# Editor Seite
@app.route('/editor')
def editor():
    return render_template('editor.html')

# MBZ Form Seite
@app.route('/mbz')
def mbz():
    lt = LibreTranslateAPI(app.config['LT_URL'])
    return render_template('mbz.html', type="MBZ",langs=lt.languages())

# XML Form Seite
@app.route('/xml')
def xml():
    lt = LibreTranslateAPI(app.config['LT_URL'])
    return render_template('xml.html', type="XML", langs=lt.languages())

# Handle Editor Content
@app.route('/get_diff_data')
def get_diff_data():
    temp_data['original'] = temp_data['original'].decode('utf-8')
    temp_data['translation'] = temp_data['translation'].decode('utf-8')
    return jsonify(temp_data)

# Handle Download
@app.route('/download')
def download():
    return temp_data['translation']

# Handle Upload
@socketio.on('upload')
def handle_upload(data):

    # Speichert die empfangenen Daten
    global temp_data
    temp_data = {
        'fileName': data['fileName'],
        'fileType': data['fileType'],
        'original': data['fileData'],
        'srcLang': data['srcLang'],
        'destLang': data['destLang']
    }
    
    # Unterschiedliche Logik je nach Dateityp
    if temp_data['fileType'] == "XML":
        # TODO: Verbessere die XML Übersetzungslogik
        try:
            temp_data['translation'] = translate_xml(app = app, url=app.config['LT_URL'] + "/translate", temp_data=temp_data)
            socketio.emit('translation_progress', {'finished': True, 'error': False})

        except Exception as e:
            socketio.emit('error', f'XML Translation Error; {temp_data['translation']}')

    elif temp_data['fileType'] == "MBZ":
        socketio.emit('log', {'message': f'MBZ-Dateien werden noch nicht unterstützt.'})
        # TODO: Implementiere die MBZ Entpack- und Übersetzungslogik
    else:
        socketio.emit('error', f'Unknown File Type: {temp_data['fileType']}')



    # # Extraktion der hochgeladenen MBZ Datei
    # if os.path.isfile(file_path):
    #     extract_mbz(file_path, app.config['EXTRACTION_FOLDER'])
 
    # # Übersetzung der extrahierten XML Dateien
    # if len(app.config["EXTRACTION_FOLDER"]) > 0:
    #     translate_mbz(app, src_lang, dest_lang)


# @socketio.on_error_default
# def default_error_handler(e):
#     print(f"Error: {e}")
#     raise Exception


if __name__ == '__main__':

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EXTRACTION_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TRANSLATION_FOLDER'], exist_ok=True)

    # Starte die Flask-SocketIO-Anwendung
    socketio.run(app=app, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)