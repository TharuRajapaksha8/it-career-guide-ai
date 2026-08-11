"""Load project configuration from the repo root .env file."""

from pathlib import Path
import os

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"


def load_env() -> None:
    """Load .env from the project root, regardless of the current working directory."""
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH, override=True)


def get_groq_api_key() -> str | None:
    """Return a cleaned Groq API key, or None if it is missing."""
    load_env()
    key = (os.getenv("GROQ_API_KEY") or "").strip().strip('"').strip("'")
    return key or None


load_env()
