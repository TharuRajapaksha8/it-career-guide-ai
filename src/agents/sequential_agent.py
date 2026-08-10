"""
Sequential Agent Pattern - Assembly Line
Agents run in order: Match → Skills → Certifications → Roadmap
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from src.agents.base_agent import BaseAgent
from src.rag.vector_store import CareerVectorStore
from src.rag.embedder import CareerEmbedder

class CareerState(TypedDict):
    """Shared state between agents"""
    user_query: str
    career_match: str      # Agent 1 writes
    skills: str            # Agent 2 writes
    certifications: str    # Agent 3 writes
    roadmap: str           # Agent 4 writes

class SequentialCareerAgent(BaseAgent):
    """Sequential assembly line of agents"""
    
    def __init__(self, model_type="groq"):
        super().__init__(model_type)
        self.vector_store = CareerVectorStore()
        self.embedder = CareerEmbedder()
    
    def _career_matcher(self, state: CareerState) -> dict:
        """Agent 1: Match career"""
        query = state["user_query"]
        
        results = self.vector_store.search(query, self.embedder, n_results=2)
        context = "\n".join([r['text'] for r in results])
        
        prompt = f"""Based on this query, identify the best IT career.

Query: {query}
Context: {context}

Return just the career name and why it fits.
"""
        response = self.llm.invoke(prompt)
        return {"career_match": response.content}
    
    def _skill_analyzer(self, state: CareerState) -> dict:
        """Agent 2: Analyze skills"""
        career = state.get("career_match", "")
        
        prompt = f"""For this career: {career}
        
List the top 5 skills needed.
Be specific about technologies and tools.
"""
        response = self.llm.invoke(prompt)
        return {"skills": response.content}
    
    def _certification_recommender(self, state: CareerState) -> dict:
        """Agent 3: Recommend certifications"""
        career = state.get("career_match", "")
        skills = state.get("skills", "")
        
        prompt = f"""For career: {career}
Skills: {skills}

Recommend 3 certifications:
1. Entry level
2. Intermediate
3. Advanced
"""
        response = self.llm.invoke(prompt)
        return {"certifications": response.content}
    
    def _roadmap_builder(self, state: CareerState) -> dict:
        """Agent 4: Build roadmap"""
        career = state.get("career_match", "")
        skills = state.get("skills", "")
        certs = state.get("certifications", "")
        
        prompt = f"""Create a 3-year roadmap for {career}.

Skills: {skills}
Certifications: {certs}

Year 1: Getting started
Year 2: Growing skills
Year 3: Advancing career
"""
        response = self.llm.invoke(prompt)
        return {"roadmap": response.content}
    
    def run(self, query):
        """Run the sequential pipeline"""
        graph = StateGraph(CareerState)
        
        graph.add_node("matcher", self._career_matcher)
        graph.add_node("skills", self._skill_analyzer)
        graph.add_node("certs", self._certification_recommender)
        graph.add_node("roadmap", self._roadmap_builder)
        
        graph.set_entry_point("matcher")
        graph.add_edge("matcher", "skills")
        graph.add_edge("skills", "certs")
        graph.add_edge("certs", "roadmap")
        graph.add_edge("roadmap", END)
        
        pipeline = graph.compile()
        result = pipeline.invoke({"user_query": query})
        
        return {"final_roadmap": result.get("roadmap", "No roadmap generated")}