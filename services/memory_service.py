from extensions import db
from models.memory import Memory


class MemoryService:
    MEMORY_TYPES = ["fact", "preference", "goal", "concern", "commitment", "decision"]

    @staticmethod
    def create(meeting_id, user_id, memory_type, content, participant_id=None, importance_score=0.0):
        m = Memory(
            meeting_id=meeting_id,
            user_id=user_id,
            memory_type=memory_type,
            content=content,
            participant_id=participant_id,
            importance_score=importance_score,
        )
        db.session.add(m)
        db.session.commit()
        return m

    @staticmethod
    def get_by_user(user_id, memory_type=None):
        query = Memory.query.filter_by(user_id=user_id)
        if memory_type:
            query = query.filter_by(memory_type=memory_type)
        return query.order_by(Memory.created_at.desc()).all()

    @staticmethod
    def get_by_participant(participant_id, user_id):
        return Memory.query.filter_by(participant_id=participant_id, user_id=user_id).order_by(Memory.created_at.desc()).all()

    @staticmethod
    def search(user_id, query_text):
        return Memory.query.filter(
            Memory.user_id == user_id,
            Memory.content.ilike(f"%{query_text}%"),
        ).all()
