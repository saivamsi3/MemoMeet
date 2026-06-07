import pytest
from main import create_app, db
from models.user import User
from models.memory import Memory
from models.meeting import Meeting
from models.participant import Participant
from models.meeting_participant import MeetingParticipant
from ai.memory_engine import MemoryEngine
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        user = User(username="test", email="test@test.com", password_hash=generate_password_hash("pass"))
        db.session.add(user)
        
        # Add some participants
        p1 = Participant(user_id=1, name="Alice Smith")
        p2 = Participant(user_id=1, name="Bob Jones")
        db.session.add_all([p1, p2])
        db.session.flush()

        # Add a meeting and map participants
        meeting = Meeting(user_id=1, title="Test Meeting", date=datetime.now(timezone.utc))
        db.session.add(meeting)
        db.session.flush()

        mp1 = MeetingParticipant(meeting_id=meeting.id, participant_id=p1.id)
        mp2 = MeetingParticipant(meeting_id=meeting.id, participant_id=p2.id)
        db.session.add_all([mp1, mp2])
        
        db.session.commit()
        yield app
        db.drop_all()


def test_create_memory(app):
    with app.app_context():
        m = Memory(meeting_id=1, user_id=1, memory_type="fact", content="Test memory", importance_score=0.5)
        db.session.add(m)
        db.session.commit()
        assert Memory.query.count() == 1


def test_parse_memories_with_attribution(app):
    with app.app_context():
        meeting = Meeting.query.get(1)
        engine = MemoryEngine()

        # Mock output from Gemini API
        gemini_result = """
FACTS:
- [Alice Smith]: Prefers coding in Python.
- [Bob Jones]: Moving to New York next week.
- [General]: The project timeline was extended by a month.
- [Alice]: Wants to take a lead role.

CONCERNS:
- [Bob]: Might not have enough bandwidth.
"""
        memories = engine._parse_result(gemini_result, meeting)

        # Check total parsed memories
        assert len(memories) == 5

        # Check facts
        facts = [m for m in memories if m["type"] == "fact"]
        assert len(facts) == 4
        
        # Verify Alice Smith mapping (name matches fully)
        m_alice = next(f for f in facts if "Prefers coding in Python" in f["content"])
        assert m_alice["participant_id"] == 1 # Alice Smith is ID 1

        # Verify Bob Jones mapping (name matches fully)
        m_bob = next(f for f in facts if "Moving to New York" in f["content"])
        assert m_bob["participant_id"] == 2 # Bob Jones is ID 2

        # Verify General mapping (no participant_id)
        m_gen = next(f for f in facts if "project timeline" in f["content"])
        assert m_gen["participant_id"] is None

        # Verify Alice mapping (fuzzy matching on "Alice")
        m_alice_fuzzy = next(f for f in facts if "lead role" in f["content"])
        assert m_alice_fuzzy["participant_id"] == 1

        # Check concern mapping (fuzzy matching on "Bob")
        concerns = [m for m in memories if m["type"] == "concern"]
        assert len(concerns) == 1
        assert concerns[0]["participant_id"] == 2
        assert "bandwidth" in concerns[0]["content"]


def test_save_memories(app):
    with app.app_context():
        meeting = Meeting.query.get(1)
        engine = MemoryEngine()

        # Mock the extraction to return pre-parsed list
        extracted_memories = [
            {"type": "fact", "content": "Prefers Python", "participant_id": 1, "importance": 0.5},
            {"type": "concern", "content": "Tight deadline", "participant_id": None, "importance": 0.7}
        ]

        def mock_extract(meet):
            return extracted_memories

        engine.extract_memories = mock_extract
        saved = engine.save_memories(meeting)

        assert len(saved) == 2
        assert Memory.query.count() == 2

        db_fact = Memory.query.filter_by(memory_type="fact").first()
        assert db_fact.participant_id == 1
        assert db_fact.content == "Prefers Python"

        db_concern = Memory.query.filter_by(memory_type="concern").first()
        assert db_concern.participant_id is None
        assert db_concern.content == "Tight deadline"
