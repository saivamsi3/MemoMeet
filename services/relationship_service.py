from main import db
from models.relationship import Relationship
from models.meeting_participant import MeetingParticipant
from models.action_item import ActionItem


class RelationshipService:
    @staticmethod
    def calculate_health_score(meeting_count, task_completion_rate, engagement_level):
        return (meeting_count * 0.3 + task_completion_rate * 0.4 + engagement_level * 0.3)

    @staticmethod
    def update_relationship(user_id, participant_id):
        meeting_count = MeetingParticipant.query.join(
            MeetingParticipant.meeting
        ).filter(
            MeetingParticipant.participant_id == participant_id,
        ).count()

        total_tasks = ActionItem.query.filter_by(participant_id=participant_id, user_id=user_id).count()
        completed_tasks = ActionItem.query.filter_by(participant_id=participant_id, user_id=user_id, status="Completed").count()
        task_completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0

        engagement_level = min(1.0, meeting_count / 10)

        health = RelationshipService.calculate_health_score(meeting_count, task_completion_rate, engagement_level)

        rel = Relationship.query.filter_by(user_id=user_id, participant_id=participant_id).first()
        if rel:
            rel.meeting_count = meeting_count
            rel.engagement_level = engagement_level
            rel.task_completion_rate = task_completion_rate
            rel.health_score = health
        else:
            rel = Relationship(
                user_id=user_id, participant_id=participant_id,
                meeting_count=meeting_count, engagement_level=engagement_level,
                task_completion_rate=task_completion_rate, health_score=health,
            )
            db.session.add(rel)
        db.session.commit()
        return rel
