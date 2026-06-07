from datetime import datetime
from main import db
from models.meeting import Meeting
from models.meeting_participant import MeetingParticipant


class MeetingService:
    @staticmethod
    def create(user_id, title, date, discussion_summary=None, key_decisions=None, action_items=None, participant_observations=None, participant_ids=None):
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        m = Meeting(
            user_id=user_id, title=title, date=date,
            discussion_summary=discussion_summary,
            key_decisions=key_decisions,
            action_items=action_items,
            participant_observations=participant_observations,
        )
        db.session.add(m)
        db.session.flush()
        if participant_ids:
            for pid in participant_ids:
                db.session.add(MeetingParticipant(meeting_id=m.id, participant_id=int(pid)))
        db.session.commit()
        return m

    @staticmethod
    def get_by_user(user_id):
        return Meeting.query.filter_by(user_id=user_id).order_by(Meeting.date.desc()).all()

    @staticmethod
    def update(meeting_id, user_id, **kwargs):
        m = Meeting.query.filter_by(id=meeting_id, user_id=user_id).first_or_404()
        participant_ids = kwargs.pop("participant_ids", None)
        for key, value in kwargs.items():
            if hasattr(m, key):
                setattr(m, key, value)
        if participant_ids is not None:
            MeetingParticipant.query.filter_by(meeting_id=m.id).delete()
            for pid in participant_ids:
                db.session.add(MeetingParticipant(meeting_id=m.id, participant_id=int(pid)))
        db.session.commit()
        return m

    @staticmethod
    def delete(meeting_id, user_id):
        m = Meeting.query.filter_by(id=meeting_id, user_id=user_id).first_or_404()
        MeetingParticipant.query.filter_by(meeting_id=m.id).delete()
        db.session.delete(m)
        db.session.commit()
