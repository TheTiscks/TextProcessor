import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("TEXTCRYPTOR_DB", str(BASE / "data.sqlite"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
