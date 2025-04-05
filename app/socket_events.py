# app/socket_events.py

import os
from flask_socketio import SocketIO
from flask import current_app
from app.translation.xml_translator import process_xml_translation

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

    # XML files
    if data['fileType'] == "text/xml":
        try:
            results = process_xml_translation(temp_data, socketio=socketio)

            temp_data['original'] = results.get("original")
            temp_data['translation'] = results.get("translation")
            temp_data['merged'] = results.get("merged")

            socketio.emit('translation_progress', {'progress': results.get("progress", 100),'finished': True})
        except Exception as e:
            socketio.emit('error', {'message': f'XML Translation Error: {e}'})

    # MBZ files are not supported yet
    elif data['fileType'] == "text/mbz":
        socketio.emit('log', {'message': 'MBZ-Dateien werden noch nicht unterstützt.'})

    # Demo 
    elif data['fileType'] == "demo":
        try:
            temp_data['fileType'] = "XML"
            demo_path = os.path.join(current_app.static_folder, "demo", "ohneKategorie.xml")
            with open(demo_path, "rb") as f:
                temp_data['original'] = f.read()

            results = process_xml_translation(temp_data, socketio=socketio)

            temp_data['original'] = results.get("original")
            temp_data['translation'] = results.get("translation")
            temp_data['merged'] = results.get("merged")

            socketio.emit('translation_progress', {'progress': results.get("progress", 100),'finished': True})
        except Exception as e:
            socketio.emit('error', {'message': f'XML Translation Error: {e}'})

    # Unsupported file types
    else:
        socketio.emit('error', {'message': f"Unbekannter Dateityp: {data['fileType']}"})
