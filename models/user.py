from extensions import db
from flask_login import UserMixin
from datetime import datetime, timezone


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    theme = db.Column(db.String(10), default="light")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    participants = db.relationship("Participant", backref="user", lazy=True)
    meetings = db.relationship("Meeting", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
