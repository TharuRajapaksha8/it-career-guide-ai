"""
Base agent with model selection
Supports Groq and OpenRouter providers.
"""

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os

class BaseAgent:
    def __init__(self, model_type="groq"):
        self.model_type = model_type
        self.llm = self._get_model()
    
    def _get_model(self):
        if self.model_type == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found")
            return ChatGroq(
                temperature=0.1,
                model="llama3-70b-8192",
                groq_api_key=api_key
            )
        elif self.model_type == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY not found")
            return ChatOpenAI(
                temperature=0.1,
                model="anthropic/claude-3.5-sonnet",
                openai_api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            api_key = os.getenv("GROQ_API_KEY")
            return ChatGroq(
                temperature=0.1,
                model="llama3-70b-8192",
                groq_api_key=api_key
            )