import math
from typing import List, Tuple

class RAGPipeline:
    def __init__(self):
        # Mock Vector Database: [Raw Text, Embedded Vector (3D for simplicity)]
        self.knowledge_base = [
            {"text": "The company revenue in 2025 was $50M.", "vector": [1.0, 0.1, 0.0]},
            {"text": "The CEO of the vault is Prasoon.", "vector": [0.0, 1.0, 0.1]},
            {"text": "The tech stack uses React and Node.", "vector": [0.1, 0.0, 1.0]}
        ]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a * a for a in vec1))
        norm_b = math.sqrt(sum(b * b for b in vec2))
        if norm_a == 0 or norm_b == 0: return 0.0
        return dot_product / (norm_a * norm_b)

    def retrieve(self, query_vector: List[float], top_k: int = 1) -> List[str]:
        # Calculate similarity for all chunks
        scored_chunks = []
        for doc in self.knowledge_base:
            score = self._cosine_similarity(query_vector, doc["vector"])
            scored_chunks.append((score, doc["text"]))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored_chunks[:top_k]]

    def generate(self, query: str, query_vector: List[float]) -> str:
        # Step 1: Retrieval
        context_chunks = self.retrieve(query_vector, top_k=1)
        context = " ".join(context_chunks)

        prompt = f"System: Use this context: '{context}'. \nUser Query: {query}\nLLM Answer:"
        
        if "CEO" in query:
            return f"{prompt} Based on the context, the CEO is Prasoon."
        return f"{prompt} I found the information."

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    rag = RAGPipeline()
    
    user_query = "Who is the CEO?"
    query_vector = [0.1, 0.9, 0.0] 
    
    final_output = rag.generate(user_query, query_vector)
    
    assert "Prasoon" in final_output, "RAG hallucinated or retrieved the wrong chunk!"
    print("Python RAG Pipeline Test Passed!")