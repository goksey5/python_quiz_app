from flask_quiz_app import create_app
from flask_quiz_app.extensions import db
from flask_quiz_app.models import Question, User, Score

# Uygulama nesnesini oluştur
app = create_app()

# Flask shell komutu ile açıldığında bu nesneler otomatik yüklenecek
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Question": Question,
        "User": User,
        "Score": Score
    }

# Sunucuyu başlat
if __name__ == '__main__':
    app.run(debug=True)
