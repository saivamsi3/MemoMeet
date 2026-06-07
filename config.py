import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///memomeet.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or ""
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or ""
    GROQ_MODEL = os.environ.get("GROQ_MODEL") or "openai/gpt-oss-120b"
    GROQ_FALLBACK_MODEL = os.environ.get("GROQ_FALLBACK_MODEL") or "qwen/qwen3-32b"
    GROQ_API_URL = os.environ.get("GROQ_API_URL") or "https://api.groq.com/openai/v1/chat/completions"
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
