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
