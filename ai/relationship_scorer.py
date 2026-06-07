from models.relationship import Relationship
from main import db


class RelationshipScorer:
    @staticmethod
    def calculate(meeting_count, task_completion_rate, engagement_level):
        return round(
            meeting_count * 0.3 +
            task_completion_rate * 0.4 +
            engagement_level * 0.3,
            2,
        )
