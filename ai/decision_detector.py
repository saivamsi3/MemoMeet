from ai.gemini_service import GeminiService


class DecisionDetector:
    def __init__(self):
        self.gemini = GeminiService()

    def detect(self, text):
        if not self.gemini.is_available():
            return self._fallback_detect(text)

        prompt = f"""
        Identify any decisions made or agreed upon in the following text.
        List each decision as a separate bullet point.

        Text:
        {text}
        """
        return self.gemini.generate(prompt)

    def _fallback_detect(self, text):
        trigger_words = ["decide", "decision", "agreed", "settled", "chosen", "elected", "opted"]
        decisions = []
        for line in text.split("."):
            if any(word in line.lower() for word in trigger_words):
                decisions.append(line.strip())
        return decisions
