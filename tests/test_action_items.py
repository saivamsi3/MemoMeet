import pytest
from main import create_app, db
from models.user import User
from models.action_item import ActionItem
from models.meeting import Meeting
from models.participant import Participant
from models.meeting_participant import MeetingParticipant
from services.action_item_service import ActionItemService
from ai.action_item_extractor import ActionItemExtractor
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone


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

        # Add a test meeting
        meeting = Meeting(user_id=user.id, title="Project Sync", date=datetime.now(timezone.utc))
        db.session.add(meeting)
        db.session.flush()

        # Add some participants linked to the meeting
        p1 = Participant(user_id=user.id, name="Sarah Connor")
        p2 = Participant(user_id=user.id, name="John Connor")
        db.session.add_all([p1, p2])
        db.session.flush()

        mp1 = MeetingParticipant(meeting_id=meeting.id, participant_id=p1.id)
        mp2 = MeetingParticipant(meeting_id=meeting.id, participant_id=p2.id)
        db.session.add_all([mp1, mp2])

        db.session.commit()
        yield app
        db.drop_all()


def test_action_item_creation(app):
    with app.app_context():
        item = ActionItem(meeting_id=1, user_id=1, task="Test task", status="Pending")
        db.session.add(item)
        db.session.commit()
        assert item.status == "Pending"


def test_action_item_extractor_parse(app):
    extractor = ActionItemExtractor()
    mock_result = """
TASK: Update the core framework | OWNER: Sarah Connor | DEADLINE: 2026-06-15
TASK: Fix database indices | OWNER: John | DEADLINE: None
TASK: Write documentation | OWNER: General | DEADLINE: 2026-06-20
"""
    items = extractor._parse(mock_result)
    assert len(items) == 3

    assert items[0]["task"] == "Update the core framework"
    assert items[0]["owner"] == "Sarah Connor"
    assert items[0]["deadline"] == "2026-06-15"

    assert items[1]["task"] == "Fix database indices"
    assert items[1]["owner"] == "John"
    assert items[1]["deadline"] is None

    assert items[2]["task"] == "Write documentation"
    assert items[2]["owner"] == "General"
    assert items[2]["deadline"] == "2026-06-20"


def test_action_item_overdue_logic(app):
    with app.app_context():
        # Create a task that is past its deadline
        past_deadline = datetime.now(timezone.utc) - timedelta(days=2)
        item1 = ActionItemService.create(
            meeting_id=1,
            user_id=1,
            task="Overdue task",
            owner="Sarah Connor",
            deadline=past_deadline.strftime("%Y-%m-%d"),
            status="Pending"
        )

        # Create a task that is in the future
        future_deadline = datetime.now(timezone.utc) + timedelta(days=5)
        item2 = ActionItemService.create(
            meeting_id=1,
            user_id=1,
            task="Future task",
            owner="John Connor",
            deadline=future_deadline.strftime("%Y-%m-%d"),
            status="Pending"
        )

        # Query items, which should trigger ActionItemService.check_overdue_tasks
        items = ActionItemService.get_by_user(user_id=1)
        
        # Check database directly
        db_item1 = ActionItem.query.filter_by(task="Overdue task").first()
        db_item2 = ActionItem.query.filter_by(task="Future task").first()

        assert db_item1.status == "Overdue"
        assert db_item2.status == "Pending"
