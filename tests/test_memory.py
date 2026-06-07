import pytest
from main import create_app, db
from models.user import User
from models.memory import Memory
from models.meeting import Meeting
from werkzeug.security import generate_password_hash
from datetime import datetime


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        user = User(username="test", email="test@test.com", password_hash=generate_password_hash("pass"))
        db.session.add(user)
        meeting = Meeting(user_id=1, title="Test", date=datetime.utcnow())
        db.session.add(meeting)
        db.session.commit()
        yield app
        db.drop_all()


def test_create_memory(app):
    with app.app_context():
        m = Memory(meeting_id=1, user_id=1, memory_type="fact", content="Test memory", importance_score=0.5)
        db.session.add(m)
        db.session.commit()
        assert Memory.query.count() == 1
