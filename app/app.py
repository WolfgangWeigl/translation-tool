import os
import secrets
import requests

from extractor import extract_mbz

from libretranslatepy import LibreTranslateAPI

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from lxml import etree as ET

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

@app.route('/')
def index():
    lt = LibreTranslateAPI(app.config['LT_URL'])
    try:
        requests.get(app.config['LT_URL'], timeout=10)
        return render_template('index.html', langs=lt.languages())
    
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {type(e).__name__}")
        return render_template('error.html', error={"type": type(e).__name__, "description": e})


@socketio.on('upload')
def handle_upload(data):
    # Empfange Daten vom Client

    file_name = data['fileName']
    file_data = data['fileData']
    src_lang = data['src']
    dest_lang = data['dest']
    
    # Speichere die hochgeladene Datei auf dem Server
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    with open(file_path, 'wb') as file:
        file.write(file_data)

    # Extraktion der hochgeladenen MBZ Datei
    if os.path.isfile(file_path):
        extract_mbz(file_path, app.config['EXTRACTION_FOLDER'])
 

    # if len(EXTRACTION_FOLDER) > 0:
    #     url = LT_URL + "translate"
    #     for (root, dirs, files) in os.walk(EXTRACTION_FOLDER):
    #         for file in files:
    #             if file.endswith('.xml'):
    #                 input_path = os.path.join(root, file)
    #                 output_path = os.path.join(TRANSLATION_FOLDER, os.path.relpath(input_path, EXTRACTION_FOLDER))
    #                 translate_xml_file(url, input_path, output_path, src_lang, dest_lang)

# @socketio.on_error_default
# def default_error_handler(e):
#     print(f"Error: {e}")
#     raise Exception

# def translate_text(url: str, text: str, source_lang: str, target_lang: str) -> str:
#     payload = {
#         "q": text,
#         "source": source_lang,
#         "target": target_lang,
#         "format": "html"
#     }

#     try:
#         response = requests.post(url, data=payload)
#         response.raise_for_status()
#         return response.json()["translatedText"]
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return

# def translate_xml_element(url: str, element: ET._Element, source_lang: str, target_lang: str):
#     try:
#         if element.text and element.text.strip():
#             if not "<script" in element.text and not "</script>" in element.text:
#                 element.text = translate_text(url=url, text=element.text, source_lang=source_lang, target_lang=target_lang)
#         for child in element:
#             translate_xml_element(element=child, source_lang=source_lang, target_lang=target_lang)
#     except Exception as e:
#         print(f"Error translating XML element: {e}")

# def translate_xml_file(url: str, input_path: str, output_path: str, source_lang: str, target_lang: str):
#     try:
#         # Parse XML
#         parser = ET.XMLParser(remove_blank_text=True)
#         tree: ET._ElementTree = ET.parse(input_path, parser)
#         root = tree.getroot()

#         # Translate
#         translate_xml_element(url=url, element=root, source_lang=source_lang, target_lang=target_lang)

#         # Save with XML declaration
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#         with open(output_path, "wb") as file:
#             file.write(ET.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True))
#         print(f"Translated XML file saved to {output_path}")

#     except ET.XMLSyntaxError as e:
#         print(f"XML syntax error: {e}")
#     except Exception as e:
#         print(f"Error processing XML file: {e}")


if __name__ == '__main__':

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EXTRACTION_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TRANSLATION_FOLDER'], exist_ok=True)

    # Starte die Flask-SocketIO-Anwendung
    socketio.run(app=app, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)