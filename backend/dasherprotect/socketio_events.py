"""
Socket.IO server events stub.
We'll emit 'hit_detected' in M3. For now, this is just a placeholder.
"""
from .extensions import socketio

@socketio.on("connect")
def on_connect():
    # You can log device_id later
    pass
