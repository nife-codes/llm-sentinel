from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime, timedelta
from typing import Optional
from . import config

class SemanticCache:
    def __init__(self):
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.cache = []
    
    def search(self, prompt: str) -> Optional[dict]:
        if not self.cache:
            return None
        
        prompt_embedding = self.model.encode(prompt)
        
        for cached_emb, cached_resp, timestamp, original_prompt in self.cache:
            if datetime.now() - timestamp > timedelta(seconds=config.CACHE_TTL_SECONDS):
                continue
            
            similarity = np.dot(prompt_embedding, cached_emb) / (
                np.linalg.norm(prompt_embedding) * np.linalg.norm(cached_emb)
            )
            
            if similarity >= config.SIMILARITY_THRESHOLD:
                return {
                    "response": cached_resp,
                    "similarity": similarity,
                    "original_prompt": original_prompt,
                }
        
        return None
    
    def add(self, prompt: str, response: dict):
        embedding = self.model.encode(prompt)
        self.cache.append((embedding, response, datetime.now(), prompt))
    
    def should_never_cache(self, prompt: str) -> bool:
        prompt_lower = prompt.lower()
        keywords = ["current", "now", "today", "latest"]
        return any(keyword in prompt_lower for keyword in keywords)
    
    def stats(self) -> dict:
        now = datetime.now()
        valid_entries = sum(
            1 for _, _, timestamp, _ in self.cache
            if now - timestamp <= timedelta(seconds=config.CACHE_TTL_SECONDS)
        )
        
        return {
            "total_entries": len(self.cache),
            "valid_entries": valid_entries,
            "expired_entries": len(self.cache) - valid_entries,
        }