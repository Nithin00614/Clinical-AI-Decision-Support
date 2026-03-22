import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Settings:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # LLM Config
    MODEL_NAME = "llama-3.1-8b-instant"
    TEMPERATURE = 0.2
    MAX_TOKENS = 500
    TIMEOUT = 10
    MAX_RETRIES = 3

    # Decision Thresholds (from your settings.md)
    SAFE_THRESHOLD = 0.3
    VERBOSE_THRESHOLD = 0.65

settings = Settings()