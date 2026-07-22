import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'development-secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/evalai')
    MONGO_DB = os.getenv('MONGO_DB', 'aase')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
