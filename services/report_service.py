from models.participant import Participant
from models.meeting import Meeting
from models.memory import Memory
from models.action_item import ActionItem
from datetime import datetime


class ReportService:
    @staticmethod
    def generate_preparation_report(meeting_id, user_id):
        meeting = Meeting.query.filter_by(id=meeting_id, user_id=user_id).first()
        if not meeting:
            return None
        participants = [mp.participant for mp in meeting.participants]
        data = {"meeting": meeting, "participants": []}
        for p in participants:
            memories = Memory.query.filter_by(participant_id=p.id, user_id=user_id).order_by(Memory.created_at.desc()).limit(10).all()
            pending = ActionItem.query.filter_by(participant_id=p.id, user_id=user_id, status="Pending").all()
            data["participants"].append({
                "participant": p,
                "memories": memories,
                "pending_items": pending,
            })
        return data
