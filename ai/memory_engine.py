from main import db
from models.memory import Memory
from ai.gemini_service import GeminiService
from ai.prompt_templates import ANALYSIS_PROMPT


class MemoryEngine:
    def __init__(self):
        self.gemini = GeminiService()

    def extract_memories(self, meeting):
        if not self.gemini.is_available():
            return self._fallback_extract(meeting)

        prompt = ANALYSIS_PROMPT.format(
            title=meeting.title,
            date=meeting.date.strftime("%Y-%m-%d"),
            summary=meeting.discussion_summary or "",
            decisions=meeting.key_decisions or "",
            actions=meeting.action_items or "",
            observations=meeting.participant_observations or "",
        )
        result = self.gemini.generate(prompt)
        return self._parse_result(result, meeting)

    def _fallback_extract(self, meeting):
        memories = []
        if meeting.key_decisions:
            for line in meeting.key_decisions.strip().split("\n"):
                if line.strip():
                    memories.append({
                        "type": "decision",
                        "content": line.strip(),
                        "importance": 0.7,
                    })
        if meeting.action_items:
            for line in meeting.action_items.strip().split("\n"):
                if line.strip():
                    memories.append({
                        "type": "commitment",
                        "content": line.strip(),
                        "importance": 0.8,
                    })
        return memories

    def _parse_result(self, result, meeting):
        memories = []
        current_type = None
        type_map = {
            "FACTS:": "fact", "CONCERNS:": "concern",
            "GOALS:": "goal", "COMMITMENTS:": "commitment",
            "PREFERENCES:": "preference", "DECISIONS:": "decision",
        }
        for line in result.split("\n"):
            line = line.strip()
            if line in type_map:
                current_type = type_map[line]
            elif line.startswith("*") or line.startswith("-"):
                content = line.lstrip("*- ").strip()
                if content and current_type:
                    memories.append({
                        "type": current_type,
                        "content": content,
                        "importance": 0.7 if current_type in ("decision", "commitment") else 0.5,
                    })
        return memories

    def save_memories(self, meeting, participant_id=None):
        extracted = self.extract_memories(meeting)
        saved = []
        for mem in extracted:
            m = Memory(
                meeting_id=meeting.id,
                user_id=meeting.user_id,
                participant_id=participant_id,
                memory_type=mem["type"],
                content=mem["content"],
                importance_score=mem.get("importance", 0.5),
            )
            db.session.add(m)
            saved.append(m)
        db.session.commit()
        return saved
