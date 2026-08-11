"""
Base agent with model selection
Supports Groq and OpenRouter providers.
"""

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
import streamlit as st

class BaseAgent:
    def __init__(self, model_type="groq"):
        self.model_type = model_type
        self.llm = self._get_model()
    
    def _get_model(self):
        # Try Streamlit secrets first, then .env
        try:
            groq_key = st.secrets.get("GROQ_API_KEY")
        except:
            groq_key = os.getenv("GROQ_API_KEY")
        
        try:
            openrouter_key = st.secrets.get("OPENROUTER_API_KEY")
        except:
            openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
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