from fastapi import FastAPI, Request
import httpx
import time
from .cache import SemanticCache
from .database import DecisionLogger
from . import config

app = FastAPI(title="Sentinel")

cache = SemanticCache()
logger = DecisionLogger()

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    prompt = body["messages"][-1]["content"]
    
    start_time = time.time()
    
    if cache.should_never_cache(prompt):
        response = await call_llm(body)
        logger.log(prompt, False, "never-cache")
        return response
    
    cached_result = cache.search(prompt)
    
    if cached_result:
        latency = int((time.time() - start_time) * 1000)
        logger.log(prompt, True, "cache-hit", cached_result["similarity"])
        
        response = cached_result["response"]
        response["x-cache-hit"] = True
        response["x-similarity"] = float(cached_result["similarity"])
        return response
    
    response = await call_llm(body)
    cache.add(prompt, response)
    logger.log(prompt, False, "cache-miss")
    
    return response

async def call_llm(body: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.LLM_BASE_URL}/chat/completions",
            json=body,
            timeout=120.0,
        )
        return response.json()

@app.get("/metrics")
async def get_metrics():
    return logger.get_metrics()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}