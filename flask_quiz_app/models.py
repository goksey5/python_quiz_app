# flask_quiz_app/models.py

from .extensions import db

# Kullanıcı modeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    highest_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)

    # Bir kullanıcının birden fazla skoru olabilir
    scores = db.relationship('Score', backref='user', lazy=True)

# Soru modeli
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # ← bunu eklemelisin

# Skor modeli
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer, nullable=False)
    
class Result(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option = db.Column(db.String(1), nullable=False)