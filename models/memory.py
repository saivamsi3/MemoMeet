from main import db
from datetime import datetime, timezone


class Memory(db.Model):
    __tablename__ = "memories"

    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    memory_type = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    importance_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    participant = db.relationship("Participant", backref="memories")

    def __repr__(self):
        return f"<Memory {self.memory_type}: {self.content[:50]}>"
