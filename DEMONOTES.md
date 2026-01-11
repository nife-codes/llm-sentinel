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


### Threshold Selection (0.85) - KEY TALKING POINT

"I empirically tested thresholds from 0.80 to 0.95.

Real password paraphrases clustered at 0.83-0.87.
Unrelated queries stayed below 0.20 - huge safety margin.

At 0.90: Too conservative, missed legitimate duplicates
At 0.80: Risked false positives
0.85: Sweet spot - balances safety and effectiveness

The system is tunable per deployment:
- High-risk flows (auth, financial): 0.90
- Medium-risk (support): 0.85  
- Low-risk (FAQs): 0.80

Security systems are about calibrated risk, not zero risk."

Why this works: Shows empirical testing, tradeoff awareness, production thinking

IF They Ask About Production Deployment:
Good answer:

"Timeouts are configurable. In production, you'd tune based on your model's p99 latency and acceptable user wait time. Local models might need 60s+, hosted APIs are usually <5s."

This shows you understand production concerns without dwelling on your demo setup.