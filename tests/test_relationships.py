import pytest
from main import create_app, db
from models.user import User
from models.relationship import Relationship
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


def test_relationship_score(app):
    with app.app_context():
        rel = Relationship(user_id=1, participant_id=1, health_score=8.5)
        db.session.add(rel)
        db.session.commit()
        assert rel.health_score == 8.5
