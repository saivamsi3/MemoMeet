from datetime import datetime, timezone
from models.participant import Participant
from models.action_item import ActionItem
from services.recommendation_service import RecommendationService


class RecommendationEngine:
    def __init__(self, user_id):
        self.user_id = user_id

    def generate_recommendations(self):
        participants = Participant.query.filter_by(user_id=self.user_id).all()
        for p in participants:
            pending = ActionItem.query.filter_by(participant_id=p.id, user_id=self.user_id, status="Pending").count()
            if pending > 3:
                RecommendationService.create(
                    user_id=self.user_id,
                    recommendation_type="unresolved_commitments",
                    content=f"{p.name} has {pending} unresolved commitments.",
                    participant_id=p.id,
                    priority="medium",
                )
