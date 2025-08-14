# Gunicorn entry-point
from dasherprotect.app import create_app
from dasherprotect.extensions import socketio

app = create_app()

# When you run with gunicorn/eventlet, SocketIO works through this app instance.
# (We don't call socketio.run here — gunicorn handles serving.)
