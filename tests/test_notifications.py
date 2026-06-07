import pytest
from datetime import datetime, timedelta, timezone
from main import create_app, db
from models.user import User
from models.meeting import Meeting
from models.participant import Participant
from models.meeting_participant import MeetingParticipant
from models.action_item import ActionItem
from models.notification import Notification
from services.notification_service import NotificationService
from services.action_item_service import ActionItemService
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        user = User(username="test", email="test@test.com", password_hash=generate_password_hash("pass"))
        db.session.add(user)
        db.session.flush()

        p = Participant(user_id=user.id, name="Sarah Connor")
        db.session.add(p)
        db.session.flush()

        db.session.commit()
        yield app
        db.drop_all()


def test_overdue_commitment_alert(app):
    with app.app_context():
        user = User.query.filter_by(username="test").first()
        # Create an overdue action item
        past_deadline = datetime.now(timezone.utc) - timedelta(days=2)
        # We need a meeting to link the action item to
        meeting = Meeting(user_id=user.id, title="Sync", date=datetime.now(timezone.utc))
        db.session.add(meeting)
        db.session.flush()

        item = ActionItem(
            meeting_id=meeting.id,
            user_id=user.id,
            task="Finish report",
            deadline=past_deadline,
            status="Pending"
        )
        db.session.add(item)
        db.session.commit()

        # Run alert generator
        NotificationService.generate_smart_alerts(user_id=user.id)

        # Check notification
        notifications = Notification.query.filter_by(
            user_id=user.id,
            notification_type="overdue_commitment"
        ).all()
        assert len(notifications) == 1
        assert "Finish report" in notifications[0].title
        assert "Finish report" in notifications[0].message

        # Running again should NOT create duplicate alerts
        NotificationService.generate_smart_alerts(user_id=user.id)
        notifications = Notification.query.filter_by(
            user_id=user.id,
            notification_type="overdue_commitment"
        ).all()
        assert len(notifications) == 1


def test_missed_followup_alert(app):
    with app.app_context():
        user = User.query.filter_by(username="test").first()
        p = Participant.query.filter_by(name="Sarah Connor").first()

        # Create a meeting dated 20 days ago
        past_date = datetime.now(timezone.utc) - timedelta(days=20)
        meeting = Meeting(user_id=user.id, title="Old Sync", date=past_date)
        db.session.add(meeting)
        db.session.flush()

        # Link participant to this meeting
        mp = MeetingParticipant(meeting_id=meeting.id, participant_id=p.id)
        db.session.add(mp)

        # Create a pending action item for this participant
        item = ActionItem(
            meeting_id=meeting.id,
            user_id=user.id,
            participant_id=p.id,
            task="Follow up with Sarah",
            deadline=datetime.now(timezone.utc) + timedelta(days=5),
            status="Pending"
        )
        db.session.add(item)
        db.session.commit()

        # Run alert generator
        NotificationService.generate_smart_alerts(user_id=user.id)

        # Check notification
        notifications = Notification.query.filter_by(
            user_id=user.id,
            notification_type="missed_followup"
        ).all()
        assert len(notifications) == 1
        assert "Sarah Connor" in notifications[0].title
