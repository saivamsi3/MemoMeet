

from main import db
from models.meeting import Meeting
from models.participant import Participant
from models.meeting_participant import MeetingParticipant
from models.user import User

def test_create_meeting(auth_client, app):
    with app.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        p1 = Participant(user_id=user.id, name="Alice Cooper")
        p2 = Participant(user_id=user.id, name="Bob Dylan")
        db.session.add_all([p1, p2])
        db.session.commit()
        p1_id = p1.id
        p2_id = p2.id

    resp = auth_client.post("/meetings/create", data={
        "title": "Strategy Sync",
        "date": "2026-06-07",
        "participants": [p1_id, p2_id],
        "discussion_summary": "Discussing goals",
        "key_decisions": "Move fast",
        "action_items": "Build MVP",
        "participant_observations": "Energetic discussions"
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Meeting created" in resp.data

    with app.app_context():
        meeting = Meeting.query.filter_by(title="Strategy Sync").first()
        assert meeting is not None
        assert len(meeting.participants) == 2
        p_ids = [mp.participant_id for mp in meeting.participants]
        assert p1_id in p_ids
        assert p2_id in p_ids


def test_edit_meeting(auth_client, app):
    with app.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        p1 = Participant(user_id=user.id, name="Alice Cooper")
        p2 = Participant(user_id=user.id, name="Bob Dylan")
        meeting = Meeting(
            user_id=user.id,
            title="Design Review",
            date=db.func.current_date(),
            discussion_summary="Old summary"
        )
        db.session.add_all([p1, p2, meeting])
        db.session.commit()
        
        mp = MeetingParticipant(meeting_id=meeting.id, participant_id=p1.id)
        db.session.add(mp)
        db.session.commit()
        
        meeting_id = meeting.id
        p2_id = p2.id

    # View edit page to ensure no errors and pre-selection logic works
    resp = auth_client.get(f"/meetings/{meeting_id}/edit")
    assert resp.status_code == 200
    assert b"checked" in resp.data  # verify participants are checked in checkbox list

    # Submit edits: swap p1 for p2, update title and summary
    resp = auth_client.post(f"/meetings/{meeting_id}/edit", data={
        "title": "Design Review Redux",
        "date": "2026-06-08",
        "participants": [p2_id],
        "discussion_summary": "New summary"
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Meeting updated" in resp.data

    with app.app_context():
        m = Meeting.query.get(meeting_id)
        assert m.title == "Design Review Redux"
        assert m.discussion_summary == "New summary"
        assert len(m.participants) == 1
        assert m.participants[0].participant_id == p2_id


def test_delete_meeting(auth_client, app):
    with app.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        meeting = Meeting(
            user_id=user.id,
            title="Temporary Meeting",
            date=db.func.current_date()
        )
        db.session.add(meeting)
        db.session.commit()
        meeting_id = meeting.id

    resp = auth_client.get(f"/meetings/{meeting_id}/delete", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Meeting deleted" in resp.data

    with app.app_context():
        m = Meeting.query.get(meeting_id)
        assert m is None


def test_search_meetings_multi_field(auth_client, app):
    with app.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        
        p = Participant(user_id=user.id, name="Charlie Brown")
        m1 = Meeting(user_id=user.id, title="Sprint Review", date=db.func.current_date(), discussion_summary="Discussing board games")
        m2 = Meeting(user_id=user.id, title="Pitch to Client", date=db.func.current_date(), key_decisions="No decisions made yet")
        
        db.session.add_all([p, m1, m2])
        db.session.commit()
        
        mp = MeetingParticipant(meeting_id=m1.id, participant_id=p.id)
        db.session.add(mp)
        db.session.commit()

    # Search by title
    resp = auth_client.get("/meetings?search=Sprint")
    assert resp.status_code == 200
    assert b"Sprint Review" in resp.data
    assert b"Pitch to Client" not in resp.data

    # Search by participant name
    resp = auth_client.get("/meetings?search=Charlie")
    assert resp.status_code == 200
    assert b"Sprint Review" in resp.data
    assert b"Pitch to Client" not in resp.data

    # Search by summary/content field
    resp = auth_client.get("/meetings?search=games")
    assert resp.status_code == 200
    assert b"Sprint Review" in resp.data
    assert b"Pitch to Client" not in resp.data

