"""
Sequential Agent Pattern - Assembly Line
Agents run in order: Match → Skills → Certifications → Roadmap
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from src.agents.base_agent import BaseAgent
from src.rag.vector_store import CareerVectorStore
from src.rag.embedder import CareerEmbedder

class CareerState(TypedDict):
    user_query: str
    career_match: str
    skills: str
    certifications: str
    roadmap: str

class SequentialCareerAgent(BaseAgent):
    def __init__(self, model_type="groq"):
        super().__init__(model_type)
        self.vector_store = CareerVectorStore()
        self.embedder = CareerEmbedder()
    
    def _career_matcher(self, state):
        query = state["user_query"]
        results = self.vector_store.search(query, self.embedder, n_results=2)
        context = "\n".join([r['text'] for r in results])
        
        prompt = f"""Based on this query, identify the best IT career.
Query: {query}
Context: {context}
Return just the career name and why it fits."""
        
        response = self.llm.invoke(prompt)
        return {"career_match": response.content}
    
    def _skill_analyzer(self, state):
        career = state.get("career_match", "")
        prompt = f"""For this career: {career}
List the top 5 skills needed. Be specific."""
        response = self.llm.invoke(prompt)
        return {"skills": response.content}
    
    def _certification_recommender(self, state):
        career = state.get("career_match", "")
        prompt = f"""For career: {career}
Recommend 3 certifications: 1 entry, 1 intermediate, 1 advanced."""
        response = self.llm.invoke(prompt)
        return {"certifications": response.content}
    
    def _roadmap_builder(self, state):
        career = state.get("career_match", "")
        prompt = f"""Create a 3-year roadmap for {career}.
Year 1: Getting started
Year 2: Growing skills
Year 3: Advancing career"""
        response = self.llm.invoke(prompt)
        return {"roadmap": response.content}
    
    def run(self, query):
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
        return {"final_roadmap": result.get("roadmap", "No roadmap")}