

def test_create_meeting(auth_client):
    resp = auth_client.post("/meetings/create", data={
        "title": "Test Meeting",
        "date": "2026-06-07",
    }, follow_redirects=True)
    assert resp.status_code == 200
