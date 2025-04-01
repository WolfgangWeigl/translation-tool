# socket_events.py

from flask_socketio import SocketIO
from flask import current_app
from translation.xml_translator import process_xml_translation

socketio = SocketIO()

temp_data = {}

@socketio.on('upload')
def handle_upload(data):
    global temp_data

    temp_data = {
        'fileName': data['fileName'],
        'fileType': data['fileType'],
        'original': data['fileData'],
        'srcLang': data['srcLang'],
        'destLang': data['destLang'],
        'transType': data['transType'],
        'url': current_app.config['LT_URL'] + "/translate"
    }

    socketio.emit('upload_progress', {'progress': 100, 'finished': True})

    if data['fileType'] == "XML":
        try:
            results = process_xml_translation(temp_data, socketio=socketio)

            # Speichern
            temp_data['original'] = results.get("original")
            temp_data['translation'] = results.get("translation")
            temp_data['merged'] = results.get("merged")

            # Fortschritt nach Abschluss
            socketio.emit('translation_progress', {
                'progress': results.get("progress", 100),
                'finished': True
            })

        except Exception as e:
            socketio.emit('error', {'message': f'XML Translation Error: {e}'})
    elif data['fileType'] == "MBZ":
        socketio.emit('log', {'message': 'MBZ-Dateien werden noch nicht unterstützt.'})
    else:
        socketio.emit('error', {'message': f"Unbekannter Dateityp: {data['fileType']}"})


@socketio.on('get_diff_data')
def get_diff_data():
    if isinstance(temp_data.get('original'), bytes):
        temp_data['original'] = temp_data['original'].decode('utf-8')
    if isinstance(temp_data.get('translation'), bytes):
        temp_data['translation'] = temp_data['translation'].decode('utf-8')
    socketio.emit('diff_data', temp_data)

@socketio.on('download')
def download():
    socketio.emit('file_data', temp_data['translation'])
