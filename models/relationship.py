from main import db
from datetime import datetime, timezone


class Relationship(db.Model):
    __tablename__ = "relationships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=False)
    meeting_count = db.Column(db.Integer, default=0)
    engagement_level = db.Column(db.Float, default=0.0)
    meeting_frequency = db.Column(db.Float, default=0.0)
    task_completion_rate = db.Column(db.Float, default=0.0)
    health_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Relationship participant={self.participant_id} score={self.health_score}>"
