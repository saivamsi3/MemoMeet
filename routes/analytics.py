from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models.meeting import Meeting
from models.participant import Participant
from models.memory import Memory
from models.action_item import ActionItem
from models.relationship import Relationship
from datetime import datetime, timedelta
from sqlalchemy import func

analytics_bp = Blueprint("analytics", __name__)


def get_analytics_context(user_id):
    total_participants = Participant.query.filter_by(user_id=user_id).count()
    total_meetings = Meeting.query.filter_by(user_id=user_id).count()
    total_memories = Memory.query.filter_by(user_id=user_id).count()
    pending = ActionItem.query.filter_by(user_id=user_id, status="Pending").count()
    in_progress = ActionItem.query.filter_by(user_id=user_id, status="In Progress").count()
    completed = ActionItem.query.filter_by(user_id=user_id, status="Completed").count()
    relationships = Relationship.query.filter_by(user_id=user_id).all()

    today = datetime.utcnow().date()
    labels = []
    counts = []
    for i in range(5, -1, -1):
        month = (today.replace(day=1) - timedelta(days=30 * i))
        start = month.replace(day=1)
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1, day=1)
        else:
            end = start.replace(month=start.month + 1, day=1)
        c = Meeting.query.filter(Meeting.user_id == user_id, Meeting.date >= start, Meeting.date < end).count()
        labels.append(start.strftime("%b %Y"))
        counts.append(c)

    total_tasks = ActionItem.query.filter_by(user_id=user_id).count()
    completed_tasks = ActionItem.query.filter_by(user_id=user_id, status="Completed").count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    comp_labels = []
    comp_rates = []
    for i in range(5, -1, -1):
        month = (today.replace(day=1) - timedelta(days=30 * i))
        start = month.replace(day=1)
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1, day=1)
        else:
            end = start.replace(month=start.month + 1, day=1)
        total_m = ActionItem.query.filter(ActionItem.user_id == user_id, ActionItem.created_at >= start, ActionItem.created_at < end).count()
        comp_m = ActionItem.query.filter(ActionItem.user_id == user_id, ActionItem.created_at >= start, ActionItem.created_at < end, ActionItem.status == "Completed").count()
        rate = (comp_m / total_m * 100) if total_m > 0 else 0
        comp_labels.append(start.strftime("%b %Y"))
        comp_rates.append(round(rate, 1))

    engagement_labels = [r.participant.name for r in relationships]
    engagement_values = [round(r.engagement_level * 100, 1) for r in relationships]

    strong = sum(1 for r in relationships if r.health_score and r.health_score > 7)
    at_risk = sum(1 for r in relationships if r.health_score and r.health_score < 4)
    moderate = len(relationships) - strong - at_risk

    upcoming_meetings = Meeting.query.filter(Meeting.user_id == user_id, Meeting.date >= datetime.utcnow()).order_by(Meeting.date).limit(5).all()

    return {
        'total_participants': total_participants,
        'total_meetings': total_meetings,
        'total_memories': total_memories,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed,
        'relationships': relationships,
        'meetings_labels': labels,
        'meetings_counts': counts,
        'completion_rate': completion_rate,
        'comp_labels': comp_labels,
        'comp_rates': comp_rates,
        'engagement_labels': engagement_labels,
        'engagement_values': engagement_values,
        'relationship_dist': {'strong': strong, 'moderate': moderate, 'at_risk': at_risk},
        'upcoming_meetings': upcoming_meetings,
    }


@analytics_bp.route("/analytics")
@login_required
def index():
    ctx = get_analytics_context(current_user.id)
    return render_template("analytics/analytics.html", **ctx)


# JSON endpoints for live charts
@analytics_bp.route("/analytics/data/meetings")
@login_required
def meetings_data():
    ctx = get_analytics_context(current_user.id)
    return jsonify(labels=ctx['meetings_labels'], counts=ctx['meetings_counts'])


@analytics_bp.route("/analytics/data/completion")
@login_required
def completion_data():
    ctx = get_analytics_context(current_user.id)
    return jsonify(labels=ctx['comp_labels'], rates=ctx['comp_rates'], overall=ctx['completion_rate'])


@analytics_bp.route("/analytics/data/engagement")
@login_required
def engagement_data():
    ctx = get_analytics_context(current_user.id)
    return jsonify(labels=ctx['engagement_labels'], values=ctx['engagement_values'])


@analytics_bp.route("/analytics/data/relationships")
@login_required
def relationships_data():
    ctx = get_analytics_context(current_user.id)
    individual_scores = [{'name': r.participant.name, 'score': r.health_score} for r in ctx['relationships']]
    return jsonify(distribution=ctx['relationship_dist'], individual_scores=individual_scores)


@analytics_bp.route("/analytics/data/tasks")
@login_required
def tasks_data():
    ctx = get_analytics_context(current_user.id)
    return jsonify(pending=ctx['pending'], in_progress=ctx['in_progress'], completed=ctx['completed'])
