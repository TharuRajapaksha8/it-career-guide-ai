"""
Simple embedder using sentence-transformers
Converts text to numbers for searching
"""

from sentence_transformers import SentenceTransformer
import numpy as np

class CareerEmbedder:
    """Converts career text to embeddings"""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None
    
    def _load_model(self):
        """Load the model (lazy loading)"""
        if self.model is None:
            print("Loading embedding model...")
            self.model = SentenceTransformer(self.model_name)
        return self.model
    
    def embed(self, text):
        """Convert text to embedding"""
        model = self._load_model()
        return model.encode(text, normalize_embeddings=True)
    
    def embed_many(self, texts):
        """Convert many texts to embeddings"""
        model = self._load_model()
        return model.encode(texts, normalize_embeddings=True)