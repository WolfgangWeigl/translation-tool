# app/wsgi.py
# pragma: no cover

from app.app import app
from app.socket_events import socketio

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
