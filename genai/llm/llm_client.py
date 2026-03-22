import os
import time
from dotenv import load_dotenv
from configs.settings import settings
from groq import Groq

load_dotenv()  # Load environment variables from .env file
class GroqLLMClient:
    """
    Real LLM client using Groq (LLaMA-3).
    """

    def __init__(self, model="llama-3.1-8b-instant"):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.MODEL_NAME

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        retries = 3

        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=500,
                    timeout=10
                )

                return response.choices[0].message.content.strip()

            except Exception as e:
                if attempt == retries - 1:
                    print(f"[LLM ERROR] Final attempt failed: {e}")
                    raise   # Reraise the exception after final attempt
                time.sleep(1)

        # Final fallback
        raise Exception("LLM service failed after retries")
