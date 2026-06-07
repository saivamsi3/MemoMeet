from extensions import db
from datetime import datetime, timezone


class Analytics(db.Model):
    __tablename__ = "analytics"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Analytics {self.metric_name}: {self.metric_value}>"
