from ai.groq_service import GroqService
from ai.prompt_templates import PREPARATION_PROMPT
from models.memory import Memory
from models.action_item import ActionItem
from models.meeting_participant import MeetingParticipant


class PreparationEngine:
    def __init__(self):
        self.gemini = GroqService()

    def generate_report(self, participant, user_id):
        meeting_count = MeetingParticipant.query.filter_by(participant_id=participant.id).count()
        memories = Memory.query.filter_by(participant_id=participant.id, user_id=user_id).order_by(Memory.created_at.desc()).limit(10).all()
        commitments = ActionItem.query.filter_by(participant_id=participant.id, user_id=user_id, status="Pending").all()

        memories_text = "\n".join(f"- [{m.memory_type}] {m.content}" for m in memories) if memories else "No memories recorded."
        commitments_text = "\n".join(f"- {c.task} (deadline: {c.deadline})" for c in commitments) if commitments else "No open commitments."

        if self.gemini.is_available():
            prompt = PREPARATION_PROMPT.format(
                participant_name=participant.name,
                health_score="N/A",
                meeting_count=meeting_count,
                memories=memories_text,
                commitments=commitments_text,
            )
            return self.gemini.generate(prompt)
        else:
            return self._generate_fallback(participant, meeting_count, memories, commitments)

    def _generate_fallback(self, participant, meeting_count, memories, commitments):
        lines = [f"--- Preparation Report for {participant.name} ---"]
        lines.append(f"\nMeetings recorded: {meeting_count}")
        if memories:
            lines.append("\nKey Memories:")
            for m in memories[:5]:
                lines.append(f"  - {m.content[:100]}")
        if commitments:
            lines.append("\nOpen Commitments:")
            for c in commitments:
                lines.append(f"  - {c.task}")
        lines.append("\nSuggested Questions:")
        lines.append("  1. How have things been since our last meeting?")
        lines.append("  2. Any updates on the topics we discussed?")
        return "\n".join(lines)
