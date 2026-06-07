import pytest
from main import db
from models.user import User
from models.meeting import Meeting
from models.participant import Participant
from models.action_item import ActionItem
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash


@pytest.fixture
def auth_client(client, app):
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password123"),
        )
        db.session.add(user)
        db.session.commit()

        # Add some mock data for tests
        p1 = Participant(user_id=user.id, name="Alice")
        p2 = Participant(user_id=user.id, name="Bob")
        db.session.add_all([p1, p2])
        db.session.flush()

        past_meeting = Meeting(
            user_id=user.id,
            title="Past Meeting",
            date=datetime.now(timezone.utc) - timedelta(days=10)
        )
        future_meeting = Meeting(
            user_id=user.id,
            title="Future Meeting",
            date=datetime.now(timezone.utc) + timedelta(days=5)
        )
        db.session.add_all([past_meeting, future_meeting])
        db.session.flush()

        item1 = ActionItem(
            meeting_id=past_meeting.id,
            user_id=user.id,
            task="Task 1",
            status="Pending"
        )
        item2 = ActionItem(
            meeting_id=past_meeting.id,
            user_id=user.id,
            task="Task 2",
            status="Completed"
        )
        db.session.add_all([item1, item2])
        db.session.commit()

    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    return client


def test_analytics_html_route(auth_client):
    resp = auth_client.get("/analytics")
    assert resp.status_code == 200
    assert b"Analytics Dashboard" in resp.data


def test_meetings_data_endpoint(auth_client):
    resp = auth_client.get("/analytics/data/meetings")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "labels" in data
    assert "counts" in data
    assert len(data["counts"]) == 6


def test_completion_data_endpoint(auth_client):
    resp = auth_client.get("/analytics/data/completion")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "labels" in data
    assert "rates" in data
    assert "overall" in data
    assert data["overall"] == 50.0  # 1 of 2 completed


def test_tasks_data_endpoint(auth_client):
    resp = auth_client.get("/analytics/data/tasks")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["pending"] == 1
    assert data["in_progress"] == 0
    assert data["completed"] == 1


def test_calendar_data_endpoint(auth_client):
    resp = auth_client.get("/analytics/data/calendar")
    assert resp.status_code == 200
    events = resp.get_json()
    assert isinstance(events, list)
    assert len(events) == 2
    titles = [e["title"] for e in events]
    assert "Past Meeting" in titles
    assert "Future Meeting" in titles
    # Verify event structure
    for event in events:
        assert "id" in event
        assert "title" in event
        assert "start" in event
        assert "url" in event
        assert "extendedProps" in event
        assert "isPast" in event["extendedProps"]
    # Past meeting should be marked as past
    past_event = next(e for e in events if e["title"] == "Past Meeting")
    assert past_event["extendedProps"]["isPast"] is True
    # Future meeting should not be past
    future_event = next(e for e in events if e["title"] == "Future Meeting")
    assert future_event["extendedProps"]["isPast"] is False
