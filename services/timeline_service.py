from models.meeting import Meeting
from models.meeting_participant import MeetingParticipant


class TimelineService:
    @staticmethod
    def get_relationship_timeline(participant_id, user_id):
        mp_ids = [mp.meeting_id for mp in MeetingParticipant.query.filter_by(participant_id=participant_id).all()]
        if not mp_ids:
            return []
        meetings = Meeting.query.filter(
            Meeting.id.in_(mp_ids),
            Meeting.user_id == user_id,
        ).order_by(Meeting.date.asc()).all()
        return meetings

    @staticmethod
    def get_meetings_for_participant(participant_id, user_id):
        # convenience wrapper (descending)
        mp_ids = [mp.meeting_id for mp in MeetingParticipant.query.filter_by(participant_id=participant_id).all()]
        if not mp_ids:
            return []
        return Meeting.query.filter(
            Meeting.id.in_(mp_ids),
            Meeting.user_id == user_id,
        ).order_by(Meeting.date.desc()).all()
