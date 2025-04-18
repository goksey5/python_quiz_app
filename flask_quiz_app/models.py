from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    highest_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.String(300), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    options = db.Column(db.PickleType)  # ['A', 'B', 'C', 'D']

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer, nullable=False)
