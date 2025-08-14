"""
Config loader. Reads from environment with safe defaults for local dev.
"""

import os

def load_config():
    return {
        "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/dasherprotect"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret-change-me"),
        "REDIS_URL": os.getenv("REDIS_URL", "redis://redis:6379/0"),
        "JSONIFY_PRETTYPRINT_REGULAR": False,
    }
