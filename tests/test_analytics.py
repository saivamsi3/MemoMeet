import pytest
from main import db
from models.user import User
from models.meeting import Meeting
from models.participant import Participant
from models.relationship import Relationship
from models.action_item import ActionItem
from datetime import datetime, timezone
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

        meeting = Meeting(
            user_id=user.id,
            title="Meeting 1",
            date=datetime.now(timezone.utc)
        )
        db.session.add(meeting)
        db.session.flush()

        rel1 = Relationship(
            user_id=user.id,
            participant_id=p1.id,
            health_score=8.0,
            engagement_level=0.8
        )
        rel2 = Relationship(
            user_id=user.id,
            participant_id=p2.id,
            health_score=3.0,
            engagement_level=0.2
        )
        db.session.add_all([rel1, rel2])

        item1 = ActionItem(
            meeting_id=meeting.id,
            user_id=user.id,
            task="Task 1",
            status="Pending"
        )
        item2 = ActionItem(
            meeting_id=meeting.id,
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
    assert data["counts"][-1] == 1  # 1 meeting this month


def test_completion_data_endpoint(auth_client):
    resp = auth_client.get("/analytics/data/completion")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "labels" in data
    assert "rates" in data
    assert "overall" in data
    assert data["overall"] == 50.0  # 1 of 2 completed


def test_engagement_data_endpoint(auth_client):
    resp = auth_client.get("/analytics/data/engagement")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "labels" in data
    assert "values" in data
    assert "Alice" in data["labels"]
    assert 80.0 in data["values"]


def test_relationships_data_endpoint(auth_client):
    resp = auth_client.get("/analytics/data/relationships")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "distribution" in data
    assert "individual_scores" in data
    assert data["distribution"]["strong"] == 1  # Alice has health_score 8.0 > 7
    assert data["distribution"]["at_risk"] == 1  # Bob has health_score 3.0 < 4
    assert len(data["individual_scores"]) == 2
    assert data["individual_scores"][0]["name"] == "Alice"
    assert data["individual_scores"][0]["score"] == 8.0


def test_tasks_data_endpoint(auth_client):
    resp = auth_client.get("/analytics/data/tasks")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["pending"] == 1
    assert data["in_progress"] == 0
    assert data["completed"] == 1
