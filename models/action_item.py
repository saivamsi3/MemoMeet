from extensions import db
from datetime import datetime, timezone


class ActionItem(db.Model):
    __tablename__ = "action_items"

    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    task = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(120), nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<ActionItem {self.task[:50]}>"
