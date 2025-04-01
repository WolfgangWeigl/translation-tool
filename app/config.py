# config.py

import os
import secrets

def configure_app(app):
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_urlsafe(16))
    app.config.update({
        'ENV': os.getenv('FLASK_ENV', 'development'),
        'DEBUG': os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes'),
        'TESTING': os.getenv('FLASK_TESTING', 'false').lower() in ('true', '1', 'yes'),
        'HOST': os.getenv('FLASK_RUN_HOST', '0.0.0.0'),
        'PORT': int(os.getenv('FLASK_RUN_PORT', '5000')),
        'UPLOAD_FOLDER': os.getenv('UPLOAD_FOLDER', '/temp/uploads'),
        'EXTRACTION_FOLDER': os.getenv('EXTRACTION_FOLDER', '/temp/extractedFiles'),
        'TRANSLATION_FOLDER': os.getenv('TRANSLATION_FOLDER', '/temp/translatedFiles'),
        'MAX_HTTP_BUFFER_SIZE': int(os.getenv('MAX_HTTP_BUFFER_SIZE', '100000000')),
        'LT_URL': os.getenv('LT_URL', 'http://libretranslate:5000')
    })
