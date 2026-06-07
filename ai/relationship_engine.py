from ai.groq_service import GroqService
from ai.prompt_templates import RECOMMENDATION_PROMPT
from models.relationship import Relationship
from models.action_item import ActionItem
from datetime import datetime, timezone


class RelationshipEngine:
    def __init__(self):
        self.gemini = GroqService()

    def analyze(self, participant, user_id):
        rel = Relationship.query.filter_by(user_id=user_id, participant_id=participant.id).first()
        if not rel:
            return {"health_score": 0, "status": "new", "suggestions": ["Schedule first meeting"]}

        status = "strong" if rel.health_score > 7 else "at-risk" if rel.health_score < 4 else "moderate"
        return {
            "health_score": round(rel.health_score, 1),
            "status": status,
            "meeting_count": rel.meeting_count,
            "engagement_level": round(rel.engagement_level, 2),
            "task_completion_rate": round(rel.task_completion_rate, 2),
        }
