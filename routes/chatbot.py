from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from ai.memory_chat_engine import MemoryChatEngine

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chat")
@login_required
def chat_page():
    return render_template("chatbot/memo_chat.html")


@chatbot_bp.route("/chat/ask", methods=["POST"])
@login_required
def ask():
    question = request.json.get("question", "")
    engine = MemoryChatEngine(current_user.id)
    answer = engine.answer(question)
    return jsonify({"answer": answer})
