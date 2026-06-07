from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.memory import Memory
from models.participant import Participant
from models.meeting import Meeting

memories_bp = Blueprint("memories", __name__)


@memories_bp.route("/memories")
@login_required
def list_memories():
    memory_type = request.args.get("type", "")
    participant_id = request.args.get("participant_id", "")
    meeting_id = request.args.get("meeting_id", "")
    importance = request.args.get("importance", "")
    q = request.args.get("q", "")

    query = Memory.query.filter_by(user_id=current_user.id)

    if memory_type:
        query = query.filter_by(memory_type=memory_type)
    
    if participant_id:
        try:
            query = query.filter_by(participant_id=int(participant_id))
        except ValueError:
            pass

    if meeting_id:
        try:
            query = query.filter_by(meeting_id=int(meeting_id))
        except ValueError:
            pass

    if importance:
        if importance == "high":
            query = query.filter(Memory.importance_score >= 0.7)
        elif importance == "medium":
            query = query.filter(Memory.importance_score >= 0.4, Memory.importance_score < 0.7)
        elif importance == "low":
            query = query.filter(Memory.importance_score < 0.4)

    if q:
        query = query.filter(Memory.content.ilike(f"%{q}%"))

    memories = query.order_by(Memory.created_at.desc()).all()

    # Fetch choices for filter dropdowns
    participants = Participant.query.filter_by(user_id=current_user.id).order_by(Participant.name.asc()).all()
    meetings = Meeting.query.filter_by(user_id=current_user.id).order_by(Meeting.date.desc()).all()

    # Calculate statistics for the dashboard cards
    stats = {
        "total": Memory.query.filter_by(user_id=current_user.id).count(),
        "fact": Memory.query.filter_by(user_id=current_user.id, memory_type="fact").count(),
        "preference": Memory.query.filter_by(user_id=current_user.id, memory_type="preference").count(),
        "goal": Memory.query.filter_by(user_id=current_user.id, memory_type="goal").count(),
        "concern": Memory.query.filter_by(user_id=current_user.id, memory_type="concern").count(),
        "commitment": Memory.query.filter_by(user_id=current_user.id, memory_type="commitment").count(),
        "decision": Memory.query.filter_by(user_id=current_user.id, memory_type="decision").count(),
    }

    return render_template(
        "memories/memories.html",
        memories=memories,
        memory_type=memory_type,
        participant_id=participant_id,
        meeting_id=meeting_id,
        importance=importance,
        q=q,
        participants=participants,
        meetings=meetings,
        stats=stats
    )


@memories_bp.route("/memories/<int:id>")
@login_required
def memory_details(id):
    memory = Memory.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template("memories/memory_details.html", memory=memory)


@memories_bp.route("/memories/<int:id>/delete", methods=["POST"])
@login_required
def delete_memory(id):
    memory = Memory.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(memory)
    db.session.commit()
    flash("Memory deleted successfully.", "success")
    return redirect(url_for("memories.list_memories"))
