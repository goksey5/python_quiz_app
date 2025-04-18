# flask_quiz_app/config.py

import os

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/quiz.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

