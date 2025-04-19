# flask_quiz_app/models.py
from .extensions import db

# Soru modeli
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)

    # Bir soruya verilen tüm cevaplar (Result tablosu ilişkisi)
    results = db.relationship('Result', back_populates='question', cascade='all, delete-orphan')


# Kullanıcı modeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    highest_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)

    # Kullanıcının verdiği tüm cevaplar (Result ile ilişki)
    results = db.relationship('Result', back_populates='user', cascade='all, delete-orphan')

    # Kullanıcının aldığı skorlar (Score ile ilişki)
    scores = db.relationship('Score', backref='user', lazy=True, cascade='all, delete-orphan')


# Skor modeli
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Cevap modeli (Result)
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=True)

    selected_option = db.Column(db.String(1), nullable=True)

    user = db.relationship('User', back_populates='results')
    question = db.relationship('Question', back_populates='results')
