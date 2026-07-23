import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
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
