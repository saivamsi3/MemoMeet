from extensions import db
from datetime import datetime, timezone


class MeetingParticipant(db.Model):
    __tablename__ = "meeting_participants"

    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
