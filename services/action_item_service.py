from datetime import datetime
from main import db
from models.action_item import ActionItem


class ActionItemService:
    @staticmethod
    def create(meeting_id, user_id, task, owner=None, deadline=None, status="Pending"):
        if isinstance(deadline, str):
            deadline = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None
        a = ActionItem(
            meeting_id=meeting_id, user_id=user_id, task=task,
            owner=owner, deadline=deadline, status=status,
        )
        db.session.add(a)
        db.session.commit()
        return a

    @staticmethod
    def get_by_user(user_id, status=None):
        query = ActionItem.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(ActionItem.deadline.asc()).all()

    @staticmethod
    def update_status(item_id, user_id, status):
        a = ActionItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
        a.status = status
        db.session.commit()
        return a
