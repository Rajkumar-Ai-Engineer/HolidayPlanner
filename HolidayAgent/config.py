import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "Prompts"

MODEL_CONFIG = {
    "model": "openai/gpt-oss-120b",
    "base_url": "https://api.groq.com/openai/v1",
    "temperature": 0.1,
    "model_info": {
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "structured_output": False,
        "family": "unknown"
    }
}

def get_api_key():
    return os.getenv("GROQ_API_KEY")
