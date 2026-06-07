from datetime import datetime, timezone
from models.action_item import ActionItem


class RiskAnalysisEngine:
    def __init__(self, user_id):
        self.user_id = user_id

    def analyze(self):
        risks = []

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
