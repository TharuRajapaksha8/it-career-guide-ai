"""
Simple document chunker for career documents
Splits documents into smaller pieces for better search
"""

import os
import re

class CareerChunker:
    """Splits career documents into chunks"""
    
    def __init__(self, chunk_size=300, overlap=30):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_file(self, file_path):
        """Read a file and split into chunks"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sections = re.split(r'\n#+\s+', content)
            chunks = []
            
            for section in sections:
                if section.strip():
                    if len(section) > self.chunk_size:
                        words = section.split()
                        for i in range(0, len(words), self.chunk_size - self.overlap):
                            chunk = ' '.join(words[i:i + self.chunk_size])
                            if chunk.strip():
                                chunks.append({
                                    'text': chunk,
                                    'source': os.path.basename(file_path)
                                })
                    else:
                        chunks.append({
                            'text': section.strip(),
                            'source': os.path.basename(file_path)
                        })
            
            return chunks
        except Exception as e:
            print(f"Error chunking {file_path}: {e}")
            return []
    
    def chunk_directory(self, dir_path):
        """Chunk all files in a directory"""
        all_chunks = []
        if not os.path.exists(dir_path):
            return all_chunks
        
        for file in os.listdir(dir_path):
            if file.endswith('.txt'):
                file_path = os.path.join(dir_path, file)
                chunks = self.chunk_file(file_path)
                all_chunks.extend(chunks)
        
        return all_chunks