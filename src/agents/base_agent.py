"""
Base agent with model selection
Supports Groq and OpenRouter providers.
"""

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from src.config import get_groq_api_key, get_openrouter_api_key  # ✅ USE CONFIG

class BaseAgent:
    def __init__(self, model_type="groq"):
        self.model_type = model_type
        self.llm = self._get_model()
    
    def _get_model(self):
        # ✅ USE CONFIG
        groq_key = get_groq_api_key()
        openrouter_key = get_openrouter_api_key()
        
        if self.model_type == "groq":
            if not groq_key:
                raise ValueError("GROQ_API_KEY not found")
            return ChatGroq(
                temperature=0.1,
                model="llama-3.3-70b-versatile",
                groq_api_key=groq_key
            )
        elif self.model_type == "openrouter":
            if not openrouter_key:
                raise ValueError("OPENROUTER_API_KEY not found")
            return ChatOpenAI(
                temperature=0.1,
                model="anthropic/claude-3.5-sonnet",
                openai_api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            if not groq_key:
                raise ValueError("GROQ_API_KEY not found")
            return ChatGroq(
                temperature=0.1,
                model="llama-3.3-70b-versatile",
                groq_api_key=groq_key
            )