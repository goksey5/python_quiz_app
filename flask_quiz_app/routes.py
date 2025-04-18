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
@quiz_bp.route('/start_quiz', methods=['GET', 'POST'])
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

        # İlk kez doğru cevap sayısı başlat
        if 'correct_count' not in session:
            session['correct_count'] = 0

        if selected_option == question.correct_option:
            session['correct_count'] += 1

        session['current_index'] += 1

    if session['current_index'] >= len(questions):
        return redirect(url_for('quiz_bp.show_result'))
    else:
        return redirect(url_for('quiz_bp.show_quiz'))


# Sonuçları gösteren sayfa – result.html
@quiz_bp.route('/result')
def show_result():
    username = session.get('username')
    correct_count = session.get('correct_count', 0)
    score = correct_count * 20  # Her doğru 20 puan

    if not username:
        return redirect(url_for('quiz_bp.index'))

    user = User.query.filter_by(username=username).first()

    if user:
        user.last_score = score
        if score > user.highest_score:
            user.highest_score = score
        db.session.commit()
        best_score = user.highest_score
    else:
        best_score = score
     # Skorları kaydet
    db.session.add(Score(username=username, score=score))
    db.session.add(Result(username=username, score=score))
    db.session.commit()

    # Genel en yüksek skoru ve sahibi
    top_result = db.session.query(Result).order_by(Result.score.desc()).first()
    global_high_score = top_result.score if top_result else 0
    global_high_scorer = top_result.username if top_result else "Henüz kimse yok"

    return render_template(
        'result.html',
        username=username,
        score=score,
        best_score=best_score,
        global_high_score=global_high_score,
        global_high_scorer=global_high_scorer
    )
# İlk 10 skoru gösteren sayfa
@quiz_bp.route('/scores')
def top_scores():
    results = Result.query.order_by(Result.score.desc()).limit(10).all()
    return render_template('scores.html', results=results, show_all=False)

# Tüm skorları listeleyen sayfa
@quiz_bp.route('/results')
def all_scores():
    results = Result.query.order_by(Result.score.desc()).all()
    return render_template('scores.html', results=results, show_all=True)

