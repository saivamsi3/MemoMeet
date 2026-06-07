from main import db
from models.analytics import Analytics
from models.meeting import Meeting
from models.participant import Participant
from models.memory import Memory
from models.action_item import ActionItem
from models.relationship import Relationship
from datetime import datetime, timezone


class AnalyticsService:
    @staticmethod
    def compute_dashboard_stats(user_id):
        return {
            "total_participants": Participant.query.filter_by(user_id=user_id).count(),
            "total_meetings": Meeting.query.filter_by(user_id=user_id).count(),
            "total_memories": Memory.query.filter_by(user_id=user_id).count(),
            "pending_tasks": ActionItem.query.filter_by(user_id=user_id, status="Pending").count(),
            "relationships": Relationship.query.filter_by(user_id=user_id).count(),
        }

    @staticmethod
    def record_metric(user_id, metric_name, metric_value):
        a = Analytics(user_id=user_id, metric_name=metric_name, metric_value=metric_value)
        db.session.add(a)
        db.session.commit()
        return a
