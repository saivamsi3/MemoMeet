from extensions import db
from models.memory import Memory
from ai.groq_service import GroqService
from ai.prompt_templates import ANALYSIS_PROMPT


class MemoryEngine:
    def __init__(self):
        self.gemini = GroqService()

    def extract_memories(self, meeting):
        participants_list = []
        for mp in meeting.participants:
            if mp.participant:
                participants_list.append(mp.participant.name)
        participants_str = ", ".join(participants_list) if participants_list else "None"

        if not self.gemini.is_available():
            return self._fallback_extract(meeting)

        prompt = ANALYSIS_PROMPT.format(
            title=meeting.title,
            date=meeting.date.strftime("%Y-%m-%d"),
            participants=participants_str,
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
        
        participants_map = {}
        for mp in meeting.participants:
            if mp.participant:
                name = mp.participant.name.strip()
                participants_map[name.lower()] = mp.participant.id

        for line in result.split("\n"):
            line = line.strip()
            if line in type_map:
                current_type = type_map[line]
            elif line.startswith("*") or line.startswith("-"):
                content = line.lstrip("*- ").strip()
                if content and current_type:
                    participant_id = None
                    if content.startswith("[") and "]" in content:
                        parts = content.split("]", 1)
                        attrib = parts[0][1:].strip()
                        rest_content = parts[1].strip()
                        if rest_content.startswith(":"):
                            rest_content = rest_content[1:].strip()
                        
                        attrib_lower = attrib.lower()
                        if attrib_lower == "general":
                            content = rest_content
                        elif attrib_lower in participants_map:
                            participant_id = participants_map[attrib_lower]
                            content = rest_content
                        else:
                            matched = False
                            for p_name, p_id in participants_map.items():
                                if p_name in attrib_lower or attrib_lower in p_name:
                                    participant_id = p_id
                                    content = rest_content
                                    matched = True
                                    break
                            if not matched:
                                pass

                    memories.append({
                        "type": current_type,
                        "content": content,
                        "participant_id": participant_id,
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
                participant_id=mem.get("participant_id") or participant_id,
                memory_type=mem["type"],
                content=mem["content"],
                importance_score=mem.get("importance", 0.5),
            )
            db.session.add(m)
            saved.append(m)
        db.session.commit()
        return saved
