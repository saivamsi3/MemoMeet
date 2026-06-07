import json
import urllib.request
import urllib.error
from config import Config


class GroqService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self.fallback_model = Config.GROQ_FALLBACK_MODEL
        self.url = Config.GROQ_API_URL

    def is_available(self):
        return bool(self.api_key)

    def _call_api(self, model, prompt, temperature):
        if self.url and "groq.com" in self.url.lower():
            if model == "openai/gpt-oss-120b":
                model = "llama-3.3-70b-versatile"
            elif model == "qwen/qwen3-32b":
                model = "llama-3.1-8b-instant"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature
        }

        req = urllib.request.Request(
            self.url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"]

    def generate(self, prompt, temperature=0.7):
        if not self.is_available():
            return "Groq API not configured. Set GROQ_API_KEY in .env"

        try:
            return self._call_api(self.model, prompt, temperature)
        except Exception as primary_error:
            if self.fallback_model and self.fallback_model != self.model:
                try:
                    return self._call_api(self.fallback_model, prompt, temperature)
                except Exception as fallback_error:
                    return f"Error (Primary model '{self.model}' failed: {str(primary_error)}. Fallback model '{self.fallback_model}' failed: {str(fallback_error)})"
            return f"Error: {str(primary_error)}"
