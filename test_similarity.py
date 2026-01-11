"""
Test: Does semantic similarity actually work?

Goal: Verify that similar prompts have high similarity scores,
and different prompts have low scores.

This validates our core assumption before we build the full system.
"""

from sentence_transformers import SentenceTransformer
import numpy as np

# Load the embedding model
# This converts text into 384-dimensional vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

# Test queries - some similar, some different
queries = [
    "How do I reset my password?",
    "I forgot my password, help",           # Similar to #1
    "What's the weather today?",            # Different
    "How do I change my password?",         # Somewhat similar to #1
    "Tell me about your refund policy",     # Different
    "What's your return policy?",           # Similar to #5
]

print("Converting text to embeddings...\n")
# Convert all queries to vectors
embeddings = model.encode(queries)

print(f"Each embedding is a vector of {len(embeddings[0])} numbers\n")
print("=" * 60)

# Calculate similarity between all pairs
for i in range(len(queries)):
    for j in range(i+1, len(queries)):
        # Cosine similarity: measures angle between vectors
        # 1.0 = identical, 0.0 = completely different
        similarity = np.dot(embeddings[i], embeddings[j]) / (
            np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
        )
        
        print(f"Query {i+1}: '{queries[i]}'")
        print(f"Query {j+1}: '{queries[j]}'")
        print(f"Similarity: {similarity:.3f}")
        
        # Interpretation
        if similarity > 0.90:
            print("→ VERY SIMILAR (would cache)")
        elif similarity > 0.70:
            print("→ Somewhat similar")
        else:
            print("→ Different (would NOT cache)")
        
        print("-" * 60)

print("\nKey insight:")
print("If similarity > 0.90, we can probably reuse the cached response")
print("If similarity < 0.90, safer to make a new API call")