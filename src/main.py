"""
Main orchestrator - manages all agents
"""

import os
from dotenv import load_dotenv
from src.agents.single_agent import SingleCareerAgent
from src.agents.sequential_agent import SequentialCareerAgent
from src.agents.parallel_agent import ParallelCareerAgent
from src.rag.chunker import CareerChunker
from src.rag.embedder import CareerEmbedder
from src.rag.vector_store import CareerVectorStore

load_dotenv()

class CareerOrchestrator:
    def __init__(self, model_type="groq"):
        self.model_type = model_type
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found")
        
        self._init_rag()
        self._init_agents()
    
    def _init_rag(self):
        self.chunker = CareerChunker()
        self.embedder = CareerEmbedder()
        self.vector_store = CareerVectorStore()
        
        if self.vector_store.collection.count() == 0:
            os.makedirs('data/knowledge_base', exist_ok=True)
            chunks = self.chunker.chunk_directory('data/knowledge_base')
            if chunks:
                embeddings = self.embedder.embed_many([c['text'] for c in chunks])
                self.vector_store.add_documents(chunks, embeddings)
    
    def _init_agents(self):
        self.single = SingleCareerAgent(self.model_type)
        self.sequential = SequentialCareerAgent(self.model_type)
        self.parallel = ParallelCareerAgent(self.model_type)
    
    def run(self, query, pattern="single"):
        patterns = {
            "single": self.single.run,
            "sequential": self.sequential.run,
            "parallel": self.parallel.run
        }
        result = patterns[pattern](query)
        result["pattern_used"] = pattern
        result["model_used"] = self.model_type
        return result

_orchestrator = None

def get_orchestrator(model_type="groq"):
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = CareerOrchestrator(model_type)
    return _orchestrator