import sys
from pathlib import Path
import pytest
from werkzeug.security import generate_password_hash


# Ensure project root is importable during pytest collection.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from main import create_app, db
from models.user import User


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def default_user(app):
    with app.app_context():
        user = User(
            username="test",
            email="test@test.com",
            password_hash=generate_password_hash("pass"),
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def auth_client(client, default_user):
    client.post("/login", data={"email": "test@test.com", "password": "pass"})
    return client
