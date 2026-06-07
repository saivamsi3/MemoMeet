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
    from services.action_item_service import ActionItemService
    from services.notification_service import NotificationService
    # Mark overdue tasks and generate smart alerts first
    ActionItemService.check_overdue_tasks(current_user.id)
    NotificationService.generate_smart_alerts(current_user.id)

    participants_count = Participant.query.filter_by(user_id=current_user.id).count()
    meetings_count = Meeting.query.filter_by(user_id=current_user.id).count()
    memories_count = Memory.query.filter_by(user_id=current_user.id).count()
    pending_tasks = ActionItem.query.filter(
        ActionItem.user_id == current_user.id,
        ActionItem.status.in_(["Pending", "In Progress", "Overdue"])
    ).count()

    recent_meetings = Meeting.query.filter_by(user_id=current_user.id).order_by(Meeting.date.desc()).limit(5).all()
    recent_memories = Memory.query.filter_by(user_id=current_user.id).order_by(Memory.created_at.desc()).limit(5).all()

    # Fetch lists for Action Item Tracker widget
    pending_action_items = ActionItem.query.filter(
        ActionItem.user_id == current_user.id,
        ActionItem.status.in_(["Pending", "In Progress", "Overdue"])
    ).order_by(ActionItem.deadline.asc().nullslast()).limit(5).all()

    from datetime import datetime, timezone
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    upcoming_deadlines = ActionItem.query.filter(
        ActionItem.user_id == current_user.id,
        ActionItem.status.in_(["Pending", "In Progress"]),
        ActionItem.deadline >= today_start
    ).order_by(ActionItem.deadline.asc()).limit(5).all()

    completed_action_items = ActionItem.query.filter_by(
        user_id=current_user.id,
        status="Completed"
    ).order_by(ActionItem.updated_at.desc()).limit(5).all()

    return render_template("dashboard/dashboard.html",
                           participants_count=participants_count,
                           meetings_count=meetings_count,
                           memories_count=memories_count,
                           pending_tasks=pending_tasks,
                           recent_meetings=recent_meetings,
                           recent_memories=recent_memories,
                           pending_action_items=pending_action_items,
                           upcoming_deadlines=upcoming_deadlines,
                           completed_action_items=completed_action_items)
