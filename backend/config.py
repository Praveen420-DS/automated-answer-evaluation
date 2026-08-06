import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))


DEVELOPMENT_SECRET_KEY = (
    "development-only-flask-secret-key-do-not-use-in-production"
)
DEVELOPMENT_JWT_SECRET_KEY = (
    "development-only-jwt-secret-key-do-not-use-in-production"
)


def validate_security_config(app_env, secret_key, jwt_secret_key):
    """Validate and resolve Flask/JWT secrets for the selected environment."""
    app_env = app_env or "development"

    if app_env.lower() == "production":
        if not secret_key:
            raise RuntimeError("SECRET_KEY is required when APP_ENV is production")
        if not jwt_secret_key:
            raise RuntimeError("JWT_SECRET_KEY is required when APP_ENV is production")
        if len(secret_key.encode("utf-8")) < 32:
            raise RuntimeError(
                "SECRET_KEY must be at least 32 bytes when APP_ENV is production"
            )
        if len(jwt_secret_key.encode("utf-8")) < 32:
            raise RuntimeError(
                "JWT_SECRET_KEY must be at least 32 bytes when APP_ENV is production"
            )
        if secret_key == jwt_secret_key:
            raise RuntimeError(
                "SECRET_KEY and JWT_SECRET_KEY must be different when APP_ENV is production"
            )
    else:
        secret_key = secret_key or DEVELOPMENT_SECRET_KEY
        jwt_secret_key = jwt_secret_key or DEVELOPMENT_JWT_SECRET_KEY

    return secret_key, jwt_secret_key


APP_ENV = os.getenv("APP_ENV", "development")
SECRET_KEY, JWT_SECRET_KEY = validate_security_config(
    APP_ENV,
    os.getenv("SECRET_KEY"),
    os.getenv("JWT_SECRET_KEY"),
)


class Config:
    APP_ENV = APP_ENV
    SECRET_KEY = SECRET_KEY
    JWT_SECRET_KEY = JWT_SECRET_KEY
    # The supplied CSV/Excel data is imported into the local ``evalai``
    # database.  Use that database by default so a fresh local run reads the
    # same records visible in MongoDB Compass.
    MONGO_DB = os.getenv("MONGO_DB", "evalai")
    MONGO_URI = os.getenv("MONGO_URI", f"mongodb://localhost:27017/{MONGO_DB}")
    # Vite uses the next available port (for example 5174) when 5173 is
    # already busy.  The local demo API uses bearer tokens, not cookies, so
    # accepting development origins is safe and prevents login preflight
    # failures when Vite changes its port.
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    ENABLE_EMBEDDING_MODEL = os.getenv("ENABLE_EMBEDDING_MODEL", "false")
    PADDLE_OCR_DEVICE = os.getenv("PADDLE_OCR_DEVICE", "cpu")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
