from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_quiz_app.config.Config')
    
    db.init_app(app)
    Migrate(app, db)

    from .routes import quiz_bp
    app.register_blueprint(quiz_bp)

    return app
