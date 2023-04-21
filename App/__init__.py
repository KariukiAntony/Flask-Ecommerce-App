from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_database(app):
    if not path.exists(f"/App/{DB_NAME}"):
        with app.app_context():
            db.create_all()
            print(f"{DB_NAME} created successfully")


def create_app():
    app = Flask(__name__)
    from .config import Config
    app.config.from_object(Config)
    db.init_app(app)
    from .views import views
    from .auth import auth
    from .uploads import uploads
    from .edit import edit
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(uploads, url_prefix="/")
    app.register_blueprint(edit, url_prefix="/")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    from .models import Trader, Product
    create_database(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Trader.query.get(int(user_id))

    return app
