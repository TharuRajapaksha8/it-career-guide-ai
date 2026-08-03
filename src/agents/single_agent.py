"""
Single Agent Pattern - ReAct Loop
One agent handles everything using reasoning + tools
"""

from langgraph.prebuilt import create_react_agent
from langchain.agents import Tool
from src.rag.vector_store import CareerVectorStore
from src.rag.embedder import CareerEmbedder
from src.agents.base_agent import BaseAgent

class SingleCareerAgent(BaseAgent):
    """Single agent that handles career questions"""
    
    def __init__(self):
        super().__init__()
        self.vector_store = CareerVectorStore()
        self.embedder = CareerEmbedder()
        
        self.system_prompt = """You are a career advisor for IT roles.
        
        When someone asks about a career, use the search tool to find information.
        Then give clear advice about:
        - What the role does
        - Skills needed
        - Certifications
        - Career path
        
        Be helpful and specific.
        """
    
    def _search_knowledge(self, query):
        """Search the knowledge base"""
        try:
            results = self.vector_store.search(query, self.embedder, n_results=3)
            if not results:
                return "No information found."
            
            output = "=== Career Information ===\n\n"
            for i, r in enumerate(results, 1):
                output += f"[{i}] {r['text']}\n\n"
            return output
        except Exception as e:
            return f"Error searching: {e}"
    
    def run(self, query):
        """Run the single agent"""
        tools = [Tool(
            name="search_knowledge",
            func=self._search_knowledge,
            description="Search for career information"
        )]
        
        agent = create_react_agent(
            model=self.llm,
            tools=tools,
            state_modifier=self.system_prompt
        )
        
        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        answer = ""
        for msg in result.get("messages", []):
            if msg.get("role") == "assistant" and not msg.get("tool_calls"):
                answer = msg.get("content", "")
                break
        
        return {"final_answer": answer}