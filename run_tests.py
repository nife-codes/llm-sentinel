"""
Send test queries to Sentinel and record results.
Tracks: response time, cache hits, similarity scores.
"""

import httpx
import time
import json
from test_queries import test_queries

BASE_URL = "http://localhost:8000"

def send_query(prompt: str):
    """Send a query and measure response time."""
    start = time.time()
    
    try:
        response = httpx.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "model": "llama3.2:1b",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=120.0
        )
        
        elapsed = time.time() - start
        data = response.json()
        
        return {
            "prompt": prompt,
            "cached": data.get("x-cache-hit", False),
            "similarity": data.get("x-similarity", 0.0),
            "latency_ms": int(elapsed * 1000),
            "tokens": data.get("usage", {}).get("total_tokens", 0),
        }
    
    except Exception as e:
        return {
            "prompt": prompt,
            "error": str(e),
            "latency_ms": int((time.time() - start) * 1000),
        }

def main():
    print("Starting Sentinel test run...")
    print(f"Testing {len(test_queries)} queries\n")
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        if not query:  # Skip empty
            continue
            
        print(f"[{i}/{len(test_queries)}] Testing: {query[:50]}...")
        result = send_query(query)
        results.append(result)
        
        # Show result
        if "error" in result:
            print(f"   Error: {result['error']}")
        elif result["cached"]:
            print(f"   CACHED (similarity: {result['similarity']:.3f}, {result['latency_ms']}ms)")
        else:
            print(f"   API CALL ({result['latency_ms']}ms, {result['tokens']} tokens)")
        
        time.sleep(0.5)  # Be nice to Ollama
    
    # Save results
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n Test complete. Results saved to test_results.json")
    
    # Summary
    cached = sum(1 for r in results if r.get("cached"))
    total = len(results)
    avg_cached_latency = sum(r["latency_ms"] for r in results if r.get("cached")) / max(cached, 1)
    avg_api_latency = sum(r["latency_ms"] for r in results if not r.get("cached")) / max(total - cached, 1)
    
    print(f"\n Summary:")
    print(f"Total queries: {total}")
    print(f"Cache hits: {cached} ({cached/total*100:.1f}%)")
    print(f"Avg latency (cached): {avg_cached_latency:.0f}ms")
    print(f"Avg latency (API): {avg_api_latency:.0f}ms")
    print(f"Speedup: {avg_api_latency/avg_cached_latency:.1f}x faster")

if __name__ == "__main__":
    main()