"""
Base agent with model selection
Uses Groq for fast responses
"""

from langchain_groq import ChatGroq
import os

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, model_type="groq"):
        """Initialize with Groq model"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Please set GROQ_API_KEY")
        
        self.llm = ChatGroq(
            temperature=0.1,
            model="llama3-70b-8192",
            groq_api_key=api_key
        )
    
    def get_response(self, prompt):
        """Get response from the model"""
        return self.llm.invoke(prompt)