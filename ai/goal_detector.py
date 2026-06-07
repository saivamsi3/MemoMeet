from ai.gemini_service import GeminiService


class GoalDetector:
    def __init__(self):
        self.gemini = GeminiService()

    def detect(self, text):
        if not self.gemini.is_available():
            return self._fallback_detect(text)

        prompt = f"""
        Identify any goals, objectives, or aspirations mentioned in the following text.
        List each goal as a separate bullet point.

        Text:
        {text}
        """
        return self.gemini.generate(prompt)

    def _fallback_detect(self, text):
        trigger_words = ["goal", "objective", "aim", "target", "aspire", "plan to", "want to", "hope to"]
        goals = []
        for line in text.split("."):
            if any(word in line.lower() for word in trigger_words):
                goals.append(line.strip())
        return goals
