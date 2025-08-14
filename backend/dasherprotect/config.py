# backend/dasherprotect/config.py
import os


def load_config() -> dict:
    """
    Read settings from environment and return a Flask config mapping.

    Accepts either SQLALCHEMY_DATABASE_URI or DATABASE_URL (Heroku-style).
    """
    db_url = os.getenv("SQLALCHEMY_DATABASE_URI") or os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "Either 'SQLALCHEMY_DATABASE_URI' or 'DATABASE_URL' must be set."
        )

    return {
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret"),
        "SQLALCHEMY_DATABASE_URI": db_url,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        # Healthy DB pools in containers
        "SQLALCHEMY_ENGINE_OPTIONS": {"pool_pre_ping": True},
        # Redis (used later for rate limiting / pubsub)
        "REDIS_URL": os.getenv("REDIS_URL", "redis://redis:6379/0"),
    }
