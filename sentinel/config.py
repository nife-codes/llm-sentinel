import os

LLM_BASE_URL = "http://localhost:11434/v1"
LLM_MODEL = "llama3.2:1b"

SIMILARITY_THRESHOLD = 0.85
CACHE_TTL_SECONDS = 3600

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DB_PATH = "sentinel_decisions.db"
API_PORT = 8000