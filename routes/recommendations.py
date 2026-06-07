from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.meeting import Meeting
from models.meeting_participant import MeetingParticipant
from models.action_item import ActionItem
from models.memory import Memory
from datetime import datetime, timezone, timedelta

recommendations_bp = Blueprint("recommendations", __name__)


def get_upcoming_meeting_recommendations(user_id):
    """
    Build actionable recommendation cards for every upcoming meeting.
    Each card contains:
      - Meeting info (title, date, days until)
      - Participants with their pending action items
      - Relevant memories/context for each participant
      - Preparation checklist items
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    upcoming = Meeting.query.filter(
        Meeting.user_id == user_id,
        Meeting.date >= now
    ).order_by(Meeting.date.asc()).all()

    meeting_cards = []
    for meeting in upcoming:
        meet_dt = meeting.date.replace(tzinfo=None) if meeting.date.tzinfo else meeting.date
        days_until = (meet_dt - now).days
        hours_until = int((meet_dt - now).total_seconds() // 3600)

        participants_data = []
        for mp in meeting.participants:
            p = mp.participant
            if not p:
                continue

            # Pending action items for this participant
            pending_items = ActionItem.query.filter_by(
                participant_id=p.id,
                user_id=user_id,
                status="Pending"
            ).order_by(ActionItem.deadline.asc()).limit(5).all()

            overdue_items = ActionItem.query.filter_by(
                participant_id=p.id,
                user_id=user_id,
                status="Overdue"
            ).limit(3).all()

            # Recent memories/context
            recent_memories = Memory.query.filter_by(
                participant_id=p.id,
                user_id=user_id
            ).order_by(Memory.created_at.desc()).limit(3).all()

            # Total meeting history count (all meetings, not just this one)
            total_meetings = MeetingParticipant.query.filter_by(
                participant_id=p.id
            ).count()

            participants_data.append({
                "participant": p,
                "pending_items": pending_items,
                "overdue_items": overdue_items,
                "recent_memories": recent_memories,
                "total_meetings": total_meetings,
            })

        # Build a preparation checklist
        checklist = []
        if not meeting.discussion_summary:
            checklist.append({"text": "Set a clear agenda / discussion summary", "done": False})
        else:
            checklist.append({"text": "Agenda/discussion summary is set", "done": True})

        total_pending = sum(len(p["pending_items"]) for p in participants_data)
        total_overdue = sum(len(p["overdue_items"]) for p in participants_data)
        if total_overdue > 0:
            checklist.append({"text": f"Review {total_overdue} overdue action item(s) before this meeting", "done": False})
        if total_pending > 0:
            checklist.append({"text": f"Follow up on {total_pending} pending commitment(s) with participants", "done": False})
        if len(participants_data) == 0:
            checklist.append({"text": "Add participants to this meeting", "done": False})
        else:
            checklist.append({"text": f"{len(participants_data)} participant(s) added", "done": True})

        # Urgency level
        if hours_until <= 24:
            urgency = "danger"
            urgency_label = "Today" if days_until == 0 else "Tomorrow"
        elif days_until <= 3:
            urgency = "warning"
            urgency_label = f"In {days_until} days"
        else:
            urgency = "primary"
            urgency_label = f"In {days_until} days"

        meeting_cards.append({
            "meeting": meeting,
            "days_until": days_until,
            "hours_until": hours_until,
            "urgency": urgency,
            "urgency_label": urgency_label,
            "participants_data": participants_data,
            "checklist": checklist,
            "total_pending": total_pending,
            "total_overdue": total_overdue,
        })

    return meeting_cards


@recommendations_bp.route("/recommendations")
@login_required
def list_recommendations():
    meeting_cards = get_upcoming_meeting_recommendations(current_user.id)
    return render_template(
        "recommendations/recommendations.html",
        meeting_cards=meeting_cards
    )
