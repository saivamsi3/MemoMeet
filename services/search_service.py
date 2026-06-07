from models.participant import Participant
from models.meeting import Meeting
from models.memory import Memory


class SearchService:
    @staticmethod
    def search(user_id, query):
        return {
            "participants": Participant.query.filter(
                Participant.user_id == user_id,
                Participant.name.ilike(f"%{query}%"),
            ).all(),
            "meetings": Meeting.query.filter(
                Meeting.user_id == user_id,
                Meeting.title.ilike(f"%{query}%"),
            ).all(),
            "memories": Memory.query.filter(
                Memory.user_id == user_id,
                Memory.content.ilike(f"%{query}%"),
            ).all(),
        }
