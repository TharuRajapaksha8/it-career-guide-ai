"""
Parallel Agent Pattern - Fan-out/Fan-in
Multiple agents research different careers simultaneously
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
import time
from src.agents.base_agent import BaseAgent
from src.rag.vector_store import CareerVectorStore
from src.rag.embedder import CareerEmbedder

class ParallelState(TypedDict):
    """Shared state for parallel agents"""
    user_query: str
    career_1: str
    career_2: str
    career_3: str
    comparison: str

class ParallelCareerAgent(BaseAgent):
    """Parallel agents researching different careers"""
    
    def __init__(self, model_type="groq"):
        super().__init__(model_type)
        self.vector_store = CareerVectorStore()
        self.embedder = CareerEmbedder()
    
    def _research_career(self, career_name, state_key):
        """Factory function for research agents"""
        def agent(state: ParallelState) -> dict:
            query = state["user_query"]
            
            results = self.vector_store.search(
                f"{career_name} {query}", 
                self.embedder, 
                n_results=2
            )
            context = "\n".join([r['text'] for r in results])
            
            prompt = f"""Research {career_name} career.

Query: {query}
Context: {context}

Provide:
1. What they do
2. Skills needed
3. Certifications
4. Career path
"""
            response = self.llm.invoke(prompt)
            return {state_key: response.content}
        return agent
    
    def _aggregator(self, state: ParallelState) -> dict:
        """Aggregator: Combine all research"""
        c1 = state.get("career_1", "")
        c2 = state.get("career_2", "")
        c3 = state.get("career_3", "")
        
        prompt = f"""Compare these 3 careers:

Career 1: {c1[:500]}
Career 2: {c2[:500]}
Career 3: {c3[:500]}

Which is best and why? Provide a clear recommendation.
"""
        response = self.llm.invoke(prompt)
        return {"comparison": response.content}
    
    def run(self, query):
        """Run parallel agents"""

        graph = StateGraph(ParallelState)
        
        def router(state):
            return {}
        
        graph.add_node("router", router)
        graph.add_node("career_1", self._research_career("Cybersecurity", "career_1"))
        graph.add_node("career_2", self._research_career("Cloud", "career_2"))
        graph.add_node("career_3", self._research_career("AI/ML", "career_3"))
        graph.add_node("aggregator", self._aggregator)
        
        graph.set_entry_point("router")
        
        graph.add_edge("router", "career_1")
        graph.add_edge("router", "career_2")
        graph.add_edge("router", "career_3")
        
        graph.add_edge("career_1", "aggregator")
        graph.add_edge("career_2", "aggregator")
        graph.add_edge("career_3", "aggregator")
        graph.add_edge("aggregator", END)
        
        pipeline = graph.compile()
        start = time.time()
        result = pipeline.invoke({"user_query": query})
        end = time.time()
        
        return {
            "final_comparison": result.get("comparison", "No comparison"),
            "execution_time": end - start
        }