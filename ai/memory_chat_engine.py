from ai.gemini_service import GeminiService
from ai.prompt_templates import CHAT_PROMPT
from models.memory import Memory
from models.meeting import Meeting
from models.action_item import ActionItem
from models.participant import Participant


class MemoryChatEngine:
    def __init__(self, user_id):
        self.user_id = user_id
        self.gemini = GeminiService()

    def _get_context(self, question):
        lines = []
        memories = Memory.query.filter_by(user_id=self.user_id).order_by(Memory.created_at.desc()).limit(20).all()
        if memories:
            lines.append("Recent Memories:")
            for m in memories:
                pname = m.participant.name if m.participant else "General"
                lines.append(f"  [{m.memory_type}] ({pname}) {m.content[:150]}")

        meetings = Meeting.query.filter_by(user_id=self.user_id).order_by(Meeting.date.desc()).limit(10).all()
        if meetings:
            lines.append("\nRecent Meetings:")
            for m in meetings:
                lines.append(f"  {m.date.strftime('%Y-%m-%d')}: {m.title}")

        items = ActionItem.query.filter_by(user_id=self.user_id).order_by(ActionItem.deadline.asc()).limit(10).all()
        if items:
            lines.append("\nAction Items:")
            for a in items:
                lines.append(f"  [{a.status}] {a.task} (owner: {a.owner or 'Unassigned'})")

        return "\n".join(lines) if lines else "No data available."

    def answer(self, question):
        context = self._get_context(question)
        if self.gemini.is_available():
            prompt = CHAT_PROMPT.format(context=context, question=question)
            return self.gemini.generate(prompt)
        return self._fallback_answer(question, context)

    def _fallback_answer(self, question, context):
        question_lower = question.lower()
        if "memory" in question_lower or "remember" in question_lower:
            return "I found these relevant memories from your database. Check the memories page for more details."
        if "meeting" in question_lower:
            return "Here are your recent meetings. You can view full details on the meetings page."
        if "commitment" in question_lower or "pending" in question_lower:
            return "Your pending commitments are listed. Visit the action items page to update them."
        return "I found some relevant information in your knowledge base. Please check the relevant sections for complete details."
