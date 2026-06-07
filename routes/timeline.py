from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.participant import Participant
from models.meeting import Meeting
from models.meeting_participant import MeetingParticipant

timeline_bp = Blueprint("timeline", __name__)


@timeline_bp.route("/timeline/<int:participant_id>")
@login_required
def relationship_timeline(participant_id):
    participant = Participant.query.filter_by(id=participant_id, user_id=current_user.id).first_or_404()
    mp_ids = [mp.meeting_id for mp in MeetingParticipant.query.filter_by(participant_id=participant_id).all()]
    meetings = Meeting.query.filter(Meeting.id.in_(mp_ids)).order_by(Meeting.date.asc()).all() if mp_ids else []
    return render_template("timeline/relationship_timeline.html", participant=participant, meetings=meetings)
