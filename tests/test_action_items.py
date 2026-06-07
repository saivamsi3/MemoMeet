import pytest
from main import create_app, db
from models.user import User
from models.action_item import ActionItem
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
        db.session.commit()
        yield app
        db.drop_all()


def test_action_item_creation(app):
    with app.app_context():
        item = ActionItem(meeting_id=1, user_id=1, task="Test task", status="Pending")
        db.session.add(item)
        db.session.commit()
        assert item.status == "Pending"
