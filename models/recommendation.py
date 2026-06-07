from extensions import db
from datetime import datetime, timezone


class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=True)
    recommendation_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default="medium")
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Recommendation {self.recommendation_type}>"
