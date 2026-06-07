from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.participant import Participant
from models.meeting import Meeting
from models.memory import Memory

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
@login_required
def search():
    q = request.args.get("q", "")
    if not q:
        return render_template("memories/memory_search.html", results=None, query=q)

    participants = Participant.query.filter(
        Participant.user_id == current_user.id,
        Participant.name.ilike(f"%{q}%"),
    ).all()

    meetings = Meeting.query.filter(
        Meeting.user_id == current_user.id,
        Meeting.title.ilike(f"%{q}%"),
    ).all()

    memories = Memory.query.filter(
        Memory.user_id == current_user.id,
        Memory.content.ilike(f"%{q}%"),
    ).all()

    return render_template("memories/memory_search.html", query=q, participants=participants, meetings=meetings, memories=memories)
