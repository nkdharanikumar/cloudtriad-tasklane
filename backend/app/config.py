"""
Application configuration.

All values are read from environment variables so nothing is hard-coded.
When you containerize this app later, just supply these as env vars
(Docker Compose env_file, Kubernetes ConfigMap/Secret, etc.).
"""
import os


class Config:
    # --- Database ---
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "taskdb")
    DB_USER = os.environ.get("DB_USER", "taskuser")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "taskpassword")

    # --- Flask ---
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # --- CORS ---
    # Comma-separated list of allowed origins. Defaults cover local Vite dev server.
    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")

    # --- Server ---
    HOST = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    PORT = int(os.environ.get("FLASK_RUN_PORT", "5000"))

    @classmethod
    def db_connection_kwargs(cls):
        """Return kwargs suitable for psycopg2.connect(...)."""
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "dbname": cls.DB_NAME,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
        }
