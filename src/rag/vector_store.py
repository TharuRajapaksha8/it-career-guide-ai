"""
Simple vector store using ChromaDB
Stores career documents for searching
"""

import chromadb
import uuid

class CareerVectorStore:
    """Stores and searches career documents"""
    
    def __init__(self, persist_dir='./chroma_db'):
        self.persist_dir = persist_dir
        
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=chromadb.Settings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="career_knowledge"
        )
        
        print(f"Vector store ready. Has {self.collection.count()} documents")
    
    def add_documents(self, chunks, embeddings):
        """Add documents to the store"""
        if not chunks:
            return
        
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        documents = [c['text'] for c in chunks]
        metadatas = [{'source': c['source']} for c in chunks]
        
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        print(f"Added {len(chunks)} documents")
    
    def search(self, query, embedder, n_results=3):
        """Search for relevant documents"""
        query_embedding = embedder.embed(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        documents = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                documents.append({
                    'text': results['documents'][0][i],
                    'source': results['metadatas'][0][i]['source']
                })
        
        return documents