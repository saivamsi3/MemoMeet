from google import genai
from google.genai import types
from config import Config


class GeminiService:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.client = None
        self.model = "gemini-2.5-flash"
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def is_available(self):
        return self.client is not None and bool(self.api_key)

    def generate(self, prompt, temperature=0.7):
        if not self.is_available():
            return "Gemini API not configured. Set GEMINI_API_KEY in .env"
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=temperature),
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
