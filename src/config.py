"""Load project configuration from the repo root .env file."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

def load_env():
    """Load .env from project root"""
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH, override=True)
    else:
        # Try current directory
        load_dotenv(override=True)

def get_groq_api_key():
    """Get Groq API key from environment"""
    load_env()
    key = os.getenv("GROQ_API_KEY", "").strip()
    if key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    if key.startswith("'") and key.endswith("'"):
        key = key[1:-1]
    return key or None

def get_openrouter_api_key():
    """Get OpenRouter API key from environment"""
    load_env()
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    if key.startswith("'") and key.endswith("'"):
        key = key[1:-1]
    return key or None