from flask import Flask

from .config import Config
from .models import db, init_db


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        init_db()
    from .routes import bp

    app.register_blueprint(bp)
    return app
