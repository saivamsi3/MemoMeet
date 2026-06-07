from datetime import datetime, timezone
from models.relationship import Relationship
from models.action_item import ActionItem


class RiskAnalysisEngine:
    def __init__(self, user_id):
        self.user_id = user_id

    def analyze(self):
        risks = []
        relationships = Relationship.query.filter_by(user_id=self.user_id).all()
        for rel in relationships:
            if rel.health_score < 4:
                risks.append({
                    "type": "at_risk_relationship",
                    "participant_id": rel.participant_id,
                    "severity": "high",
                    "message": f"Relationship health score is critically low ({rel.health_score:.1f})",
                })

        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        overdue = ActionItem.query.filter(
            ActionItem.user_id == self.user_id,
            ActionItem.status.in_(["Pending", "In Progress"]),
            ActionItem.deadline < today_start,
        ).count()
        if overdue > 0:
            risks.append({
                "type": "overdue_tasks",
                "severity": "medium",
                "message": f"{overdue} action items are overdue",
            })

        return risks
