from ai.groq_service import GroqService


class PreferenceDetector:
    def __init__(self):
        self.gemini = GroqService()

    def detect(self, text):
        if not self.gemini.is_available():
            return self._fallback_detect(text)

        prompt = f"""
        Identify any preferences, likes, or dislikes expressed in the following text.
        List each preference as a separate bullet point.

        Text:
        {text}
        """
        return self.gemini.generate(prompt)

    def _fallback_detect(self, text):
        trigger_words = ["prefer", "like", "dislike", "want", "would rather", "preference"]
        preferences = []
        for line in text.split("."):
            if any(word in line.lower() for word in trigger_words):
                preferences.append(line.strip())
        return preferences
