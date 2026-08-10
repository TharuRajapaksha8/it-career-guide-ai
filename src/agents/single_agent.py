from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools import tool
from src.rag.vector_store import CareerVectorStore
from src.rag.embedder import CareerEmbedder
from src.agents.base_agent import BaseAgent

class SingleCareerAgent(BaseAgent):
    def __init__(self, model_type="groq"):
        super().__init__(model_type)
        self.vector_store = CareerVectorStore()
        self.embedder = CareerEmbedder()
        
        self.system_prompt = """You are a career advisor for IT roles.
        When someone asks about a career, use the search tool to find information.
        Give clear advice about: what the role does, skills needed, certifications, and career path."""
    
    def _search_knowledge(self, query):
        try:
            results = self.vector_store.search(query, self.embedder, n_results=3)
            if not results:
                return "No information found."
            output = "Career Information:\n\n"
            for i, r in enumerate(results, 1):
                output += f"[{i}] {r['text']}\n\n"
            return output
        except Exception as e:
            return f"Error searching: {e}"
    
    def run(self, query):
        tools = [Tool(
            name="search_knowledge",
            func=self._search_knowledge,
            description="Search for career information"
        )]
        
        agent = create_react_agent(
            model=self.llm,
            tools=[search_knowledge],
            prompt=self.system_prompt
        )
        
        result = agent.invoke({
            "messages": [HumanMessage(content=query)]
        })
        
        answer = ""
        for msg in result.get("messages", []):
            if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
                answer = msg.content
                break
        
        return {"final_answer": answer or "No answer generated"}