from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.memory import Memory

memories_bp = Blueprint("memories", __name__)


@memories_bp.route("/memories")
@login_required
def list_memories():
    memory_type = request.args.get("type", "")
    query = Memory.query.filter_by(user_id=current_user.id)
    if memory_type:
        query = query.filter_by(memory_type=memory_type)
    memories = query.order_by(Memory.created_at.desc()).all()
    return render_template("memories/memories.html", memories=memories, memory_type=memory_type)


@memories_bp.route("/memories/<int:id>")
@login_required
def memory_details(id):
    memory = Memory.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template("memories/memory_details.html", memory=memory)
