# app/app.py

from flask import Flask, render_template, jsonify
from app.config import configure_app
from app.socket_events import socketio
from app.utils.file_utils import ensure_directories

app = Flask(__name__)
configure_app(app)

socketio.init_app(app,
    max_http_buffer_size=app.config['MAX_HTTP_BUFFER_SIZE'],
    logger=True,
    async_mode='eventlet'
)

# Verzeichnisse sicherstellen
ensure_directories(
    app.config['UPLOAD_FOLDER'],
    app.config['EXTRACTION_FOLDER'],
    app.config['TRANSLATION_FOLDER']
)

@app.route('/')
def index():
    return render_template('index.html', current_page='home')

@app.route('/guide')
def guide():
    return render_template('guide.html', current_page='guide')

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/get_diff_data')
def get_diff_data():
    from app.socket_events import temp_data

    original = temp_data.get("original")
    translation = temp_data.get("translation")

    if isinstance(original, bytes):
        original = original.decode("utf-8")
    if isinstance(translation, bytes):
        translation = translation.decode("utf-8")

    return jsonify({
        "original": original,
        "translation": translation
    })

@app.route('/xml')
def xml():
    from libretranslatepy import LibreTranslateAPI
    lt = LibreTranslateAPI(app.config['LT_URL'])
    langs = lt.languages()
    return render_template('xml.html', current_page='home',type="XML", langs=sorted(langs, key=lambda x: x["name"]))

@app.route('/mbz')
def mbz():
    from libretranslatepy import LibreTranslateAPI
    lt = LibreTranslateAPI(app.config['LT_URL'])
    langs = lt.languages()
    return render_template('mbz.html', current_page='home', type="MBZ", langs=sorted(langs, key=lambda x: x["name"]))

@app.route('/download')
def download():
    from app.socket_events import temp_data

    if temp_data.get('transType') == 'multiple':
        merged = temp_data.get("merged")
        return merged.decode('utf-8') if isinstance(merged, bytes) else merged

    translated = temp_data.get("translation")
    return translated.decode('utf-8') if isinstance(translated, bytes) else translated

def run_app():
    socketio.run(app=app, host=app.config['HOST'], port=app.config['PORT'], allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    run_app()
