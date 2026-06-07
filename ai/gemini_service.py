import google.generativeai as genai
from config import Config


class GeminiService:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model = None
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")

    def is_available(self):
        return self.model is not None and bool(self.api_key)

    def generate(self, prompt, temperature=0.7):
        if not self.is_available():
            return "Gemini API not configured. Set GEMINI_API_KEY in .env"
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
