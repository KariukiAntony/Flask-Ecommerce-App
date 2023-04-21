from . import DB_NAME


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = "new project"
    SESSION_PERMANENT = False
