from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    encrypted = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    views_left = db.Column(db.Integer, nullable=False, default=1)
    webhook = db.Column(db.Text, nullable=True)

def init_db():
    db.create_all()