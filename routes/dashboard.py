from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.participant import Participant
from models.meeting import Meeting
from models.memory import Memory
from models.action_item import ActionItem

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    participants_count = Participant.query.filter_by(user_id=current_user.id).count()
    meetings_count = Meeting.query.filter_by(user_id=current_user.id).count()
    memories_count = Memory.query.filter_by(user_id=current_user.id).count()
    pending_tasks = ActionItem.query.filter_by(user_id=current_user.id, status="Pending").count()

    recent_meetings = Meeting.query.filter_by(user_id=current_user.id).order_by(Meeting.date.desc()).limit(5).all()
    recent_memories = Memory.query.filter_by(user_id=current_user.id).order_by(Memory.created_at.desc()).limit(5).all()

    return render_template("dashboard/dashboard.html",
                           participants_count=participants_count,
                           meetings_count=meetings_count,
                           memories_count=memories_count,
                           pending_tasks=pending_tasks,
                           recent_meetings=recent_meetings,
                           recent_memories=recent_memories)
