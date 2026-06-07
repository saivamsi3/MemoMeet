from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.meeting import Meeting
from models.participant import Participant
from models.memory import Memory
from models.action_item import ActionItem
from models.relationship import Relationship

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
@login_required
def index():
    total_participants = Participant.query.filter_by(user_id=current_user.id).count()
    total_meetings = Meeting.query.filter_by(user_id=current_user.id).count()
    total_memories = Memory.query.filter_by(user_id=current_user.id).count()
    pending = ActionItem.query.filter_by(user_id=current_user.id, status="Pending").count()
    in_progress = ActionItem.query.filter_by(user_id=current_user.id, status="In Progress").count()
    completed = ActionItem.query.filter_by(user_id=current_user.id, status="Completed").count()
    relationships = Relationship.query.filter_by(user_id=current_user.id).all()

    return render_template("analytics/analytics.html",
                           total_participants=total_participants,
                           total_meetings=total_meetings,
                           total_memories=total_memories,
                           pending=pending,
                           in_progress=in_progress,
                           completed=completed,
                           relationships=relationships)
