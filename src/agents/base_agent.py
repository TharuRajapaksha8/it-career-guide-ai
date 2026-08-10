"""
Base agent with model selection
Supports Groq and OpenRouter providers.
"""

from langchain_groq import ChatGroq

from src.config import get_groq_api_key

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, model_type="groq"):
        """Initialize the selected model backend"""
        self.model_type = model_type.lower()

        if self.model_type == "groq":
            api_key = get_groq_api_key()
            if not api_key:
                raise ValueError("Please set GROQ_API_KEY in .env")
            self.llm = ChatGroq(
                temperature=0.1,
                model="llama-3.3-70b-versatile",
                api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")
    
    def get_response(self, prompt):
        """Get response from the model"""
        return self.llm.invoke(prompt)