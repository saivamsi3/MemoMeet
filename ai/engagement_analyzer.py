from datetime import datetime, timezone
from models.meeting import Meeting
from models.meeting_participant import MeetingParticipant


class EngagementAnalyzer:
    def __init__(self, user_id):
        self.user_id = user_id

    def analyze_participant_engagement(self, participant_id):
        mp_ids = [mp.meeting_id for mp in MeetingParticipant.query.filter_by(participant_id=participant_id).all()]
        if not mp_ids:
            return 0
        meetings = Meeting.query.filter(Meeting.id.in_(mp_ids), Meeting.user_id == self.user_id).order_by(Meeting.date.desc()).all()
        if not meetings:
            return 0
        days_since = (datetime.now(timezone.utc) - meetings[0].date).days if meetings[0].date else 365
        recency = max(0, 1 - days_since / 365)
        frequency = min(1, len(meetings) / 10)
        return round((recency + frequency) / 2, 2)
