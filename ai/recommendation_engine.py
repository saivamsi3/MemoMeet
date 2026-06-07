from datetime import datetime, timezone
from models.relationship import Relationship
from models.meeting import Meeting
from models.action_item import ActionItem
from services.recommendation_service import RecommendationService


class RecommendationEngine:
    def __init__(self, user_id):
        self.user_id = user_id

    def generate_recommendations(self):
        relationships = Relationship.query.filter_by(user_id=self.user_id).all()
        for rel in relationships:
            if rel.health_score < 4:
                RecommendationService.create(
                    user_id=self.user_id,
                    recommendation_type="at_risk_relationship",
                    content=f"Relationship with {rel.participant.name} needs attention. Score: {rel.health_score:.1f}",
                    participant_id=rel.participant_id,
                    priority="high",
                )

            pending = ActionItem.query.filter_by(participant_id=rel.participant_id, user_id=self.user_id, status="Pending").count()
            if pending > 3:
                RecommendationService.create(
                    user_id=self.user_id,
                    recommendation_type="unresolved_commitments",
                    content=f"{rel.participant.name} has {pending} unresolved commitments.",
                    participant_id=rel.participant_id,
                    priority="medium",
                )
