from main import db
from models.user import User
from werkzeug.security import generate_password_hash


def test_register(client):
    resp = client.post("/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }, follow_redirects=True)
    assert resp.status_code == 200


def test_login(client, app):
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password123"),
        )
        db.session.add(user)
        db.session.commit()

    resp = client.post("/login", data={
        "email": "test@example.com",
        "password": "password123",
    }, follow_redirects=True)
    assert resp.status_code == 200


def test_logout(client, app):
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password123"),
        )
        db.session.add(user)
        db.session.commit()

    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    resp = client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200
