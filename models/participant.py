from extensions import db
from datetime import datetime, timezone


class Participant(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    organization = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(120), nullable=True)
    interests = db.Column(db.Text, nullable=True)
    goals = db.Column(db.Text, nullable=True)
    preferences = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    meetings = db.relationship("MeetingParticipant", backref="participant", lazy=True)

    def __repr__(self):
        return f"<Participant {self.name}>"
