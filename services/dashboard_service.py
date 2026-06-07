from models.participant import Participant
from models.meeting import Meeting
from models.memory import Memory
from models.action_item import ActionItem


class DashboardService:
    @staticmethod
    def get_stats(user_id):
        return {
            "participants": Participant.query.filter_by(user_id=user_id).count(),
            "meetings": Meeting.query.filter_by(user_id=user_id).count(),
            "memories": Memory.query.filter_by(user_id=user_id).count(),
            "pending": ActionItem.query.filter_by(user_id=user_id, status="Pending").count(),
        }

    @staticmethod
    def get_recent_meetings(user_id, limit=5):
        return Meeting.query.filter_by(user_id=user_id).order_by(Meeting.date.desc()).limit(limit).all()
