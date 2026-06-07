from extensions import db
from models.user import User
from models.participant import Participant
from models.meeting import Meeting
from models.meeting_participant import MeetingParticipant
from models.memory import Memory
from models.action_item import ActionItem
from models.recommendation import Recommendation
from models.notification import Notification
from models.analytics import Analytics


def init_db():
    db.create_all()


def drop_db():
    db.drop_all()
