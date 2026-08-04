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
    """Orchestrates all agents"""
    
    def __init__(self):
        
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY in .env")
        
        self._init_rag()
        self._init_agents()
        
        print("Orchestrator ready!")
    
    def _init_rag(self):
        """Set up RAG pipeline"""
        print("Setting up RAG...")
        self.chunker = CareerChunker()
        self.embedder = CareerEmbedder()
        self.vector_store = CareerVectorStore()
        
        if self.vector_store.collection.count() == 0:
            print("Loading career documents...")
            os.makedirs('data/knowledge_base', exist_ok=True)
            chunks = self.chunker.chunk_directory('data/knowledge_base')
            
            if chunks:
                embeddings = self.embedder.embed_many([c['text'] for c in chunks])
                self.vector_store.add_documents(chunks, embeddings)
                print(f"Loaded {len(chunks)} documents")
    
    def _init_agents(self):
        """Initialize all agents"""
        print("Initializing agents...")
        self.single = SingleCareerAgent()
        self.sequential = SequentialCareerAgent()
        self.parallel = ParallelCareerAgent()
    
    def run(self, query, pattern="single"):
        """Run with selected pattern"""
        patterns = {
            "single": self.single.run,
            "sequential": self.sequential.run,
            "parallel": self.parallel.run
        }
        
        if pattern not in patterns:
            return {"error": "Invalid pattern"}
        
        result = patterns[pattern](query)
        result["pattern_used"] = pattern
        return result

_orchestrator = None

def get_orchestrator():
    """Get or create orchestrator"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = CareerOrchestrator()
    return _orchestrator