from ai.groq_service import GroqService


class CommitmentDetector:
    def __init__(self):
        self.gemini = GroqService()

    def detect(self, text):
        if not self.gemini.is_available():
            return self._fallback_detect(text)

        prompt = f"""
        Identify any commitments, promises, or agreed action items in the following text.
        For each, identify who committed and what they committed to.

        Text:
        {text}
        """
        return self.gemini.generate(prompt)

    def _fallback_detect(self, text):
        trigger_words = ["will", "promise", "commit", "agree", "shall", "going to", "plan to"]
        commitments = []
        for line in text.split("."):
            if any(word in line.lower() for word in trigger_words):
                commitments.append(line.strip())
        return commitments
