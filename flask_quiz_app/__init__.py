# flask_quiz_app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint'i buraya doğru şekilde import et
    from .routes import quiz_bp
    app.register_blueprint(quiz_bp)

    return app

