from datetime import datetime, timezone
from extensions import db
from models.action_item import ActionItem
from services.relationship_service import RelationshipService


class ActionItemService:
    @staticmethod
    def create(meeting_id, user_id, task, owner=None, deadline=None, status="Pending", participant_id=None):
        if isinstance(deadline, str):
            deadline = deadline.strip()
            if deadline and deadline.lower() != "none":
                try:
                    deadline = datetime.strptime(deadline, "%Y-%m-%d")
                except ValueError:
                    deadline = None
            else:
                deadline = None
        
        a = ActionItem(
            meeting_id=meeting_id,
            user_id=user_id,
            task=task,
            owner=owner,
            deadline=deadline,
            status=status,
            participant_id=participant_id
        )
        db.session.add(a)
        db.session.commit()
        # Update relationship metrics if this action item is linked to a participant
        if participant_id:
            RelationshipService.update_relationship(user_id, participant_id)
        return a

    @staticmethod
    def check_overdue_tasks(user_id):
        # Update overdue tasks: status in Pending or In Progress with past deadline
        # Deadlines are only considered overdue after the deadline day has fully passed.
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        overdue_items = ActionItem.query.filter(
            ActionItem.user_id == user_id,
            ActionItem.status.in_(["Pending", "In Progress"]),
            ActionItem.deadline < today_start
        ).all()
        for item in overdue_items:
            item.status = "Overdue"
        if overdue_items:
            db.session.commit()

    @staticmethod
    def get_by_user(user_id, status=None):
        # Automatically mark past due tasks as Overdue
        ActionItemService.check_overdue_tasks(user_id)

        query = ActionItem.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(ActionItem.deadline.asc().nullslast()).all()

    @staticmethod
    def update_status(item_id, user_id, status):
        a = ActionItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
        a.status = status
        db.session.commit()
        # Update relationship metrics if linked
        if a.participant_id:
            RelationshipService.update_relationship(user_id, a.participant_id)
        return a
