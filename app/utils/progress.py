# utils/progress.py

def emit_progress(socketio, current, total, channel='translation_progress'):
    if not socketio or total == 0:
        return
    progress = round((current / total) * 100, 2)
    socketio.emit(channel, {'progress': progress, 'finished': False})
