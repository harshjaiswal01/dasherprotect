# Gunicorn config w/ eventlet for Socket.IO
workers = 1
worker_class = "eventlet"
bind = "0.0.0.0:5001"
timeout = 120
accesslog = "-"
errorlog = "-"
