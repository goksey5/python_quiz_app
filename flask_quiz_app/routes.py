from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import db, User, Question, Score, Result
import random

# Blueprint tanımlıyoruz: 'quiz_bp' adında bir grup URL tanımı yapacağız
quiz_bp = Blueprint('quiz_bp', __name__)

# Kullanıcı giriş sayfası – index.html
@quiz_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        if username:
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username)
                db.session.add(user)
                db.session.commit()
            session['username'] = username
            return redirect(url_for('quiz_bp.start_quiz'))
    return render_template('index.html')

# Quiz başlatma – kullanıcının sorularla buluşması
@quiz_bp.route('/start_quiz')
def start_quiz():
    questions = Question.query.all()
    if len(questions) < 5:
        return "Yeterli sayıda soru yok. Lütfen veri tabanına daha fazla soru ekleyin."
    
    selected_questions = random.sample(questions, 5)
    session['questions'] = [q.id for q in selected_questions]
    session['current_index'] = 0
    session['score'] = 0
    return redirect(url_for('quiz_bp.show_quiz'))

# Quiz sorularını sırayla gösteren sayfa – quiz_form.html
@quiz_bp.route('/quiz', methods=['GET'])
def show_quiz():
    current_index = session.get('current_index', 0)
    questions = session.get('questions', [])

    if current_index >= len(questions):
        return redirect(url_for('quiz_bp.show_result'))

    question_id = questions[current_index]
    question = Question.query.get(question_id)
    return render_template('quiz_form.html', question=question, question_number=current_index + 1)

# Kullanıcının verdiği cevapları değerlendirme
@quiz_bp.route('/submit_answers', methods=['POST'])
def submit_answers():
    selected_option = request.form.get('option')
    current_index = session.get('current_index', 0)
    questions = session.get('questions', [])

    if current_index < len(questions):
        question_id = questions[current_index]
        question = Question.query.get(question_id)

        if selected_option == question.correct_option:
            session['score'] += 1

        session['current_index'] += 1

    if session['current_index'] >= len(questions):
        return redirect(url_for('quiz_bp.show_result'))
    else:
        return redirect(url_for('quiz_bp.show_quiz'))

# Sonuçları gösteren sayfa – result.html
@quiz_bp.route('/result')
def show_result():
    username = session.get('username')
    score = session.get('score', 0)

    if not username:
        return redirect(url_for('quiz_bp.index'))

    user = User.query.filter_by(username=username).first()
    if user:
        user.last_score = score
        if score > user.highest_score:
            user.highest_score = score
        db.session.commit()

    result = Result(username=username, score=score)
    db.session.add(result)
    db.session.commit()

    return render_template('result.html', username=username, score=score)

# Tüm kullanıcıların sonuçlarını listeleyen sayfa – scores.html
@quiz_bp.route('/scores')
def show_scores():
    results = Result.query.order_by(Result.score.desc()).limit(10).all()
    return render_template('scores.html', results=results)
