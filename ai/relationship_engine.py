from models.meeting_participant import MeetingParticipant


class RelationshipEngine:
    """Relationship scoring has been removed. This engine now returns basic meeting count data."""

    def analyze(self, participant, user_id):
        meeting_count = MeetingParticipant.query.filter_by(participant_id=participant.id).count()
        return {
            "health_score": 0,
            "status": "new" if meeting_count == 0 else "active",
            "meeting_count": meeting_count,
        }
