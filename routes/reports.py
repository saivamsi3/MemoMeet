from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.participant import Participant
from models.meeting import Meeting
from models.memory import Memory
from models.relationship import Relationship

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/preparation/<int:meeting_id>")
@login_required
def preparation_report(meeting_id):
    meeting = Meeting.query.filter_by(id=meeting_id, user_id=current_user.id).first_or_404()
    return render_template("reports/preparation_report.html", meeting=meeting)


@reports_bp.route("/reports/participant/<int:participant_id>")
@login_required
def participant_report(participant_id):
    participant = Participant.query.filter_by(id=participant_id, user_id=current_user.id).first_or_404()
    memories = Memory.query.filter_by(participant_id=participant_id, user_id=current_user.id).all()
    relationship = Relationship.query.filter_by(participant_id=participant_id, user_id=current_user.id).first()
    return render_template("reports/participant_report.html", participant=participant, memories=memories, relationship=relationship)
