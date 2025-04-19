from flask_quiz_app import create_app
from flask_quiz_app.extensions import db
from flask_quiz_app.models import Question, User, Score, Result  # ← Result'ı ekle

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Question": Question,
        "User": User,
        "Score": Score,
        "Result": Result   # ← Shell için Result da eklendi
    }

if __name__ == '__main__':
    app.run(debug=True)
