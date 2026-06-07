from main import db
from models.participant import Participant


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


def test_search_participants_multi_field(auth_client, app):
    with app.app_context():
        from models.user import User
        user = User.query.filter_by(email="test@test.com").first()
        # Create test participants
        p1 = Participant(user_id=user.id, name="Alice Smith", organization="Google", interests="AI, Coding")
        p2 = Participant(user_id=user.id, name="Bob Jones", organization="Microsoft", goals="Scaling, Growth")
        db.session.add_all([p1, p2])
        db.session.commit()
        
    # Search by organization
    resp = auth_client.get("/participants?search=Google")
    assert resp.status_code == 200
    assert b"Alice Smith" in resp.data
    assert b"Bob Jones" not in resp.data

    # Search by interests
    resp = auth_client.get("/participants?search=Coding")
    assert resp.status_code == 200
    assert b"Alice Smith" in resp.data
    assert b"Bob Jones" not in resp.data

    # Search by goals
    resp = auth_client.get("/participants?search=Scaling")
    assert resp.status_code == 200
    assert b"Bob Jones" in resp.data
    assert b"Alice Smith" not in resp.data


def test_toggle_theme(auth_client, app):
    # Test valid theme toggles via JSON
    resp = auth_client.post("/settings/toggle-theme", json={"theme": "dark"})
    assert resp.status_code == 200
    assert resp.json["status"] == "success"
    assert resp.json["theme"] == "dark"

    with app.app_context():
        from models.user import User
        user = User.query.filter_by(email="test@test.com").first()
        assert user.theme == "dark"

    resp = auth_client.post("/settings/toggle-theme", json={"theme": "light"})
    assert resp.status_code == 200
    assert resp.json["theme"] == "light"

    # Test invalid theme toggles
    resp = auth_client.post("/settings/toggle-theme", json={"theme": "invalid-theme"})
    assert resp.status_code == 400

