from typing import List, Dict, Any
import numpy as np
import json
from pathlib import Path

class VectorDB:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.vectors = []  # List of (vector, metadata) tuples
        self.dimension = None
        
    def add_vector(self, vector: List[float], metadata: Dict[str, Any]):
        """Thêm một vector và metadata tương ứng vào database"""
        if self.dimension is None:
            self.dimension = len(vector)
        elif len(vector) != self.dimension:
            raise ValueError(f"Vector dimension mismatch. Expected {self.dimension}, got {len(vector)}")
            
        self.vectors.append({
            "vector": vector,
            "metadata": metadata
        })
        
    def save(self):
        """Lưu vector database xuống file"""
        with open(self.db_path / "vectors.json", "w", encoding="utf-8") as f:
            json.dump({
                "dimension": self.dimension,
                "vectors": self.vectors
            }, f, ensure_ascii=False, indent=2)
            
    def load(self):
        """Load vector database từ file"""
        if (self.db_path / "vectors.json").exists():
            with open(self.db_path / "vectors.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.dimension = data["dimension"]
                self.vectors = data["vectors"]
                
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """Tìm kiếm top_k vectors gần nhất với query vector"""
        if len(self.vectors) == 0:
            return []
            
        query_vector = np.array(query_vector)
        db_vectors = np.array([v["vector"] for v in self.vectors])
        
        similarities = np.dot(db_vectors, query_vector) / (
            np.linalg.norm(db_vectors, axis=1) * np.linalg.norm(query_vector)
        )
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "score": float(similarities[idx]),
                "metadata": self.vectors[idx]["metadata"]
            })
            
        return results
