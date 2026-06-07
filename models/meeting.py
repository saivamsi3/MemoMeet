from extensions import db
from datetime import datetime, timezone


class Meeting(db.Model):
    __tablename__ = "meetings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    discussion_summary = db.Column(db.Text, nullable=True)
    key_decisions = db.Column(db.Text, nullable=True)
    action_items = db.Column(db.Text, nullable=True)
    participant_observations = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    participants = db.relationship("MeetingParticipant", backref="meeting", lazy=True)
    memories = db.relationship("Memory", backref="meeting", lazy=True)

    def __repr__(self):
        return f"<Meeting {self.title}>"
