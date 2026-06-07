from extensions import db


def run_migrations():
    from models.user import User
    from models.participant import Participant
    from models.meeting import Meeting
    from models.meeting_participant import MeetingParticipant
    from models.memory import Memory
    from models.action_item import ActionItem
    from models.relationship import Relationship
    from models.recommendation import Recommendation
    from models.notification import Notification
    from models.analytics import Analytics

    db.create_all()
