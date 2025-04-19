import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını yükle

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///quiz.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


