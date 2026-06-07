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
