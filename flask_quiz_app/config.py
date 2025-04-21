import os
from dotenv import load_dotenv

load_dotenv()  

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///D:/python_quiz_app/instance/quiz.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


