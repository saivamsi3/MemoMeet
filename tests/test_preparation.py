from ai.preparation_engine import PreparationEngine
from models.participant import Participant


def test_preparation_fallback(app):
    # create a dummy participant-like object
    class DummyParticipant:
        def __init__(self, id, name):
            self.id = id
            self.name = name

    p = DummyParticipant(1, "Test User")
    engine = PreparationEngine()
    # Ensure fallback generator returns a string even when Gemini unavailable
    text = engine._generate_fallback(p, None, [], [])
    assert isinstance(text, str)
    assert "Preparation Report" in text
