# flask_quiz_app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import quiz_bp
    app.register_blueprint(quiz_bp)

    return app

