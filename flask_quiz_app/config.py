import os
from dotenv import load_dotenv

load_dotenv()  

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    # Veritabanı yolunu PythonAnywhere ortamına uygun hale getirin
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///instance/quiz.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


