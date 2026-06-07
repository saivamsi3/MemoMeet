from extensions import db
from models.notification import Notification


class NotificationService:
    @staticmethod
    def create(user_id, notification_type, title, message=None):
        n = Notification(
            user_id=user_id, notification_type=notification_type,
            title=title, message=message,
        )
        db.session.add(n)
        db.session.commit()
        return n

    @staticmethod
    def get_by_user(user_id, unread_only=False):
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        return query.order_by(Notification.created_at.desc()).all()

    @staticmethod
    def mark_read(notification_id, user_id):
        n = Notification.query.filter_by(id=notification_id, user_id=user_id).first_or_404()
        n.is_read = True
        db.session.commit()
        return n

    @staticmethod
    def generate_smart_alerts(user_id):
        from datetime import datetime, timezone
        from models.user import User
        from models.action_item import ActionItem
        from models.relationship import Relationship
        from models.participant import Participant
        from models.meeting_participant import MeetingParticipant
        from models.meeting import Meeting
        from services.action_item_service import ActionItemService

        # 1. Update/check overdue tasks status
        ActionItemService.check_overdue_tasks(user_id)

        # 2. Generate Overdue Commitment alerts
        overdue_items = ActionItem.query.filter_by(user_id=user_id, status="Overdue").all()
        for item in overdue_items:
            title = f"Overdue Commitment: {item.task}"
            existing = Notification.query.filter_by(
                user_id=user_id,
                notification_type="overdue_commitment",
                title=title
            ).first()
            if not existing:
                due_date_str = item.deadline.strftime("%Y-%m-%d") if item.deadline else "unknown"
                message = f"Action item '{item.task}' (Owner: {item.owner or 'Unassigned'}) was due on {due_date_str}."
                NotificationService.create(
                    user_id=user_id,
                    notification_type="overdue_commitment",
                    title=title,
                    message=message
                )

        # 3. Generate Missed Follow-up alerts
        now = datetime.utcnow()
        participants = Participant.query.filter_by(user_id=user_id).all()
        for p in participants:
            mp_meetings = Meeting.query.join(MeetingParticipant).filter(
                MeetingParticipant.participant_id == p.id,
                Meeting.user_id == user_id
            ).all()
            if not mp_meetings:
                continue

            # Check past/future meetings with naive comparison
            past_meetings = [m for m in mp_meetings if m.date and m.date.replace(tzinfo=None) <= now]
            future_meetings = [m for m in mp_meetings if m.date and m.date.replace(tzinfo=None) > now]

            if not future_meetings and past_meetings:
                latest_meeting = max(past_meetings, key=lambda x: x.date)
                m_date = latest_meeting.date.replace(tzinfo=None)
                days_since = (now - m_date).days
                if days_since > 14:
                    has_pending_items = ActionItem.query.filter(
                        ActionItem.user_id == user_id,
                        ActionItem.participant_id == p.id,
                        ActionItem.status.in_(["Pending", "In Progress", "Overdue"])
                    ).count() > 0

                    if has_pending_items:
                        title = f"Missed Follow-up with {p.name}"
                        existing = Notification.query.filter_by(
                            user_id=user_id,
                            notification_type="missed_followup",
                            title=title
                        ).first()
                        if not existing:
                            message = f"It has been {days_since} days since your last meeting with {p.name} on {latest_meeting.date.strftime('%Y-%m-%d')}, and there are open action items."
                            NotificationService.create(
                                user_id=user_id,
                                notification_type="missed_followup",
                                title=title,
                                message=message
                            )

        # 4. Generate Declining Engagement alerts
        relationships = Relationship.query.filter_by(user_id=user_id).all()
        for r in relationships:
            if r.health_score < 4.0 or r.engagement_level < 0.3:
                title = f"Declining Engagement: {r.participant.name}"
                existing = Notification.query.filter_by(
                    user_id=user_id,
                    notification_type="declining_engagement",
                    title=title
                ).first()
                if not existing:
                    message = f"Relationship health score with {r.participant.name} is low ({r.health_score:.1f}/10.0). Engagement level is {r.engagement_level * 100:.1f}%. Consider scheduling a catch-up."
                    NotificationService.create(
                        user_id=user_id,
                        notification_type="declining_engagement",
                        title=title,
                        message=message
                    )

