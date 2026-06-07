from extensions import db
from models.relationship import Relationship
from models.meeting_participant import MeetingParticipant
from models.action_item import ActionItem
from models.meeting import Meeting
from datetime import datetime, timezone


class RelationshipService:
    @staticmethod
    def calculate_health_score(frequency_score, completion_score, recency_score):
        return (frequency_score * 0.3 + completion_score * 0.4 + recency_score * 0.3)

    @staticmethod
    def update_relationship(user_id, participant_id):
        # 1. Frequency Score (based on meeting count, min 5 meetings for max score)
        meeting_count = MeetingParticipant.query.join(
            MeetingParticipant.meeting
        ).filter(
            MeetingParticipant.participant_id == participant_id,
        ).count()
        frequency_score = min(10.0, meeting_count * 2.0)

        # 2. Completion Score (based on task completion rate, defaults to 8.0 if no tasks exist)
        total_tasks = ActionItem.query.filter_by(participant_id=participant_id, user_id=user_id).count()
        completed_tasks = ActionItem.query.filter_by(participant_id=participant_id, user_id=user_id, status="Completed").count()
        
        task_completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0
        if total_tasks > 0:
            completion_score = task_completion_rate * 10.0
        else:
            completion_score = 8.0

        # 3. Recency Score (based on days since last meeting)
        last_mp = MeetingParticipant.query.join(MeetingParticipant.meeting)\
            .filter(MeetingParticipant.participant_id == participant_id)\
            .order_by(Meeting.date.desc()).first()
            
        if last_mp and last_mp.meeting.date:
            meet_date = last_mp.meeting.date
            if meet_date.tzinfo is not None:
                now_time = datetime.now(timezone.utc)
            else:
                now_time = datetime.now(timezone.utc).replace(tzinfo=None)
                
            days_since = (now_time - meet_date).days
            if days_since <= 7:
                recency_score = 10.0
            elif days_since <= 14:
                recency_score = 8.0
            elif days_since <= 30:
                recency_score = 6.0
            elif days_since <= 60:
                recency_score = 4.0
            else:
                recency_score = 2.0
        else:
            recency_score = 0.0

        # 4. Calculate final composite health score (0-10.0)
        health = RelationshipService.calculate_health_score(frequency_score, completion_score, recency_score)

        # Engagement level is mapped between 0.0 and 1.0 (recency_score / 10.0)
        engagement_level = recency_score / 10.0

        rel = Relationship.query.filter_by(user_id=user_id, participant_id=participant_id).first()
        if rel:
            rel.meeting_count = meeting_count
            rel.engagement_level = engagement_level
            rel.meeting_frequency = frequency_score
            rel.task_completion_rate = task_completion_rate
            rel.health_score = health
        else:
            rel = Relationship(
                user_id=user_id, participant_id=participant_id,
                meeting_count=meeting_count, engagement_level=engagement_level,
                meeting_frequency=frequency_score,
                task_completion_rate=task_completion_rate, health_score=health,
            )
            db.session.add(rel)
        db.session.commit()
        return rel
