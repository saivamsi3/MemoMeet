from ai.gemini_service import GeminiService


class ConcernDetector:
    def __init__(self):
        self.gemini = GeminiService()

    def detect(self, text):
        if not self.gemini.is_available():
            return self._fallback_detect(text)

        prompt = f"""
        Identify any concerns, risks, or worries expressed in the following text.
        List each concern as a separate bullet point.

        Text:
        {text}
        """
        return self.gemini.generate(prompt)

    def _fallback_detect(self, text):
        trigger_words = ["concern", "worry", "risk", "issue", "problem", "challenge", "difficult"]
        concerns = []
        for line in text.split("."):
            if any(word in line.lower() for word in trigger_words):
                concerns.append(line.strip())
        return concerns
