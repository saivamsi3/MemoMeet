from ai.groq_service import GroqService
from ai.prompt_templates import PREPARATION_PROMPT
from models.memory import Memory
from models.action_item import ActionItem
from models.relationship import Relationship
from services.relationship_service import RelationshipService


class PreparationEngine:
    def __init__(self):
        self.gemini = GroqService()

    def generate_report(self, participant, user_id):
        rel = Relationship.query.filter_by(user_id=user_id, participant_id=participant.id).first()
        memories = Memory.query.filter_by(participant_id=participant.id, user_id=user_id).order_by(Memory.created_at.desc()).limit(10).all()
        commitments = ActionItem.query.filter_by(participant_id=participant.id, user_id=user_id, status="Pending").all()

        memories_text = "\n".join(f"- [{m.memory_type}] {m.content}" for m in memories) if memories else "No memories recorded."
        commitments_text = "\n".join(f"- {c.task} (deadline: {c.deadline})" for c in commitments) if commitments else "No open commitments."

        if self.gemini.is_available():
            prompt = PREPARATION_PROMPT.format(
                participant_name=participant.name,
                health_score=rel.health_score if rel else "N/A",
                meeting_count=rel.meeting_count if rel else 0,
                memories=memories_text,
                commitments=commitments_text,
            )
            return self.gemini.generate(prompt)
        else:
            return self._generate_fallback(participant, rel, memories, commitments)

    def _generate_fallback(self, participant, rel, memories, commitments):
        lines = [f"--- Preparation Report for {participant.name} ---"]
        lines.append(f"\nRelationship Health: {rel.health_score:.1f}/10" if rel else "\nRelationship: New contact")
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
