import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    MONGO_DB = os.getenv("MONGO_DB", "aase")
    MONGO_URI = os.getenv("MONGO_URI", f"mongodb://localhost:27017/{MONGO_DB}")
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    ENABLE_EMBEDDING_MODEL = os.getenv("ENABLE_EMBEDDING_MODEL", "false")
    PADDLE_OCR_DEVICE = os.getenv("PADDLE_OCR_DEVICE", "cpu")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
