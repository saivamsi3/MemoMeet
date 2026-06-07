from ai.gemini_service import GeminiService


class ActionItemExtractor:
    def __init__(self):
        self.gemini = GeminiService()

    def extract(self, text):
        if not self.gemini.is_available():
            return self._fallback_extract(text)

        prompt = f"""
        Extract action items from the following text.
        For each action item, identify: task description, owner (if mentioned), and deadline (if mentioned).

        Text:
        {text}

        Format each action item as: TASK: | OWNER: | DEADLINE:
        """
        result = self.gemini.generate(prompt)
        return self._parse(result)

    def _fallback_extract(self, text):
        items = []
        for line in text.strip().split("\n"):
            line = line.strip()
            if line and (line.startswith("-") or line.startswith("*") or line[0].isdigit()):
                items.append({"task": line.lstrip("-*0123456789. ").strip(), "owner": None, "deadline": None})
        return items

    def _parse(self, result):
        items = []
        for line in result.split("\n"):
            line = line.strip()
            if line.startswith("TASK:"):
                parts = line.split("|")
                task = parts[0].replace("TASK:", "").strip()
                owner = parts[1].replace("OWNER:", "").strip() if len(parts) > 1 else None
                deadline = parts[2].replace("DEADLINE:", "").strip() if len(parts) > 2 else None
                items.append({"task": task, "owner": owner, "deadline": deadline})
        return items
