from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import db, User, Question, Score, Result
import random

quiz_bp = Blueprint('quiz_bp', __name__)

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
        else:
            flash("Lütfen bir kullanıcı adı girin.", "warning")
    return render_template('index.html')

@quiz_bp.route('/start_quiz', methods=['GET', 'POST'])
def start_quiz():
    questions = Question.query.all()
    print(f"Veritabanındaki Sorular: {questions}")
    
    if len(questions) < 5:
        return "Yeterli sayıda soru yok. Lütfen veri tabanına daha fazla soru ekleyin."
    
    selected_questions = random.sample(questions, 5)
    session['questions'] = [q.id for q in selected_questions]
    session['current_index'] = 0
    session['score'] = 0

    print(f"start_quiz - Selected Questions: {session['questions']}")
    print(f"start_quiz - Current Index: {session['current_index']}")
    print(f"start_quiz - Oturum Durumu: {session}")

    return redirect(url_for('quiz_bp.show_quiz'))



@quiz_bp.route('/quiz', methods=['GET'])
def show_quiz():
    username = session.get('username')
    if not username:
        flash("Kullanıcı adı oturumda bulunamadı. Lütfen tekrar giriş yapın.", "warning")
        return redirect(url_for('quiz_bp.index'))

    if 'questions' not in session:
        flash("Sorular oturumda bulunamadı, lütfen tekrar quiz başlatın.", "danger")
        return redirect(url_for('quiz_bp.start_quiz'))
    
    questions = Question.query.filter(Question.id.in_(session['questions'])).all()

    print(f"show_quiz - Sorular: {questions}")
    
 

    return render_template('quiz_form.html', questions=questions, username=username)




@quiz_bp.route('/submit_answers', methods=['POST'])

def submit_answers():
   
    username = session.get('username')

    if not username:
        flash("Kullanıcı adı oturumda bulunamadı. Lütfen giriş yapın.", "warning")
        return redirect(url_for('quiz_bp.index'))

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()  

    questions = Question.query.all()
    correct_count = 0

    for question in questions:
        selected_option = request.form.get(f'question_{question.id}')

        if selected_option == question.correct_option:
            correct_count += 20

        result = Result(user=user, question_id=question.id, selected_option=selected_option)
        db.session.add(result)
    
    score = Score(user=user, score=correct_count)
    db.session.add(score)
    db.session.commit()

    session['score'] = correct_count
    print("Gelen form verileri:", dict(request.form))
    return redirect(url_for('quiz_bp.show_result'))

    


@quiz_bp.route('/result')
def show_result():
    username = session.get('username')
    score = session.get('score', 0)

    if not username:
        flash("Kullanıcı adı oturumda bulunamadı. Lütfen giriş yapın.", "warning")
        return redirect(url_for('quiz_bp.index'))

    user = User.query.filter_by(username=username).first()

    if user:
        if score > user.highest_score:
            user.highest_score = score
        db.session.commit()
        best_score = user.highest_score
    else:
        best_score = score

    top_score = db.session.query(Score).order_by(Score.score.desc()).first()
    global_high_score = top_score.score if top_score else 0
    global_high_scorer = top_score.user.username if top_score and top_score.user else "Henüz kimse yok"

    return render_template(
        'result.html',
        username=username,
        score=score,
        best_score=best_score,
        global_high_score=global_high_score,
        global_high_scorer=global_high_scorer
    )


@quiz_bp.route('/scores')
def top_scores():
    results = Score.query.order_by(Score.score.desc()).limit(10).all()
    return render_template('scores.html', results=results, show_all=False)


@quiz_bp.route('/results')
def all_scores():
    results = Score.query.order_by(Score.score.desc()).all()
    return render_template('scores.html', results=results, show_all=True)
