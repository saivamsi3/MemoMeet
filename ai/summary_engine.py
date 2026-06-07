from ai.groq_service import GroqService


class SummaryEngine:
    def __init__(self):
        self.gemini = GroqService()

    def generate_summary(self, meeting):
        if not self.gemini.is_available():
            return meeting.discussion_summary or "No summary available."

        prompt = f"""
        Summarize the following meeting in 3-5 key points:

        Title: {meeting.title}
        Discussion: {meeting.discussion_summary or "Not provided"}
        Decisions: {meeting.key_decisions or "Not provided"}
        """
        return self.gemini.generate(prompt)
