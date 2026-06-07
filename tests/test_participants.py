import pytest
from main import create_app, db
from models.user import User
from models.participant import Participant
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


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    client.post("/login", data={"email": "test@test.com", "password": "pass"})
    return client


def test_add_participant(auth_client):
    resp = auth_client.post("/participants/add", data={"name": "John Doe", "email": "john@example.com"}, follow_redirects=True)
    assert resp.status_code == 200


def test_list_participants(auth_client, app):
    with app.app_context():
        p = Participant(user_id=1, name="Jane Doe")
        db.session.add(p)
        db.session.commit()
    resp = auth_client.get("/participants")
    assert resp.status_code == 200
