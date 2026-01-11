# Sentinel Demo - Talking Points

## Opening (30 seconds)
"Sentinel is a decision and audit layer for LLM infrastructure.
It sits between apps and LLM providers, decides when API calls 
are necessary, and logs everything for audit."

## Model Modularity Point (IMPORTANT)
"The model is swappable by design. I used Ollama during the sprint
for reliability and zero cost, but in production you'd point this
at GPT-4, Claude, or any OpenAI-compatible endpoint."

## When They Ask About Threshold
"I chose 0.95 because false positives are more expensive than 
false negatives. Tested 0.90-0.99, found 0.95 gave best balance."

## Things NOT to say:
- Don't apologize for using local model
- Don't say "I ran out of time for X"
- Don't overexplain the obvious

## Demo Flow:
1. Show config (model swappability)
2. Run simulation (watch cache build)
3. Show metrics (hit rate, cost saved)
4. Show decision log (explainability)
5. Answer questions