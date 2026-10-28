# Module 7 solutions — Architecture: the blueprint

1. (a) Cache hit: cache check + feedback log = 10 ms, 0.02 units.
   (b) Blocked: cache check + guardrail check = 15 ms, 0.03 units.
   (c) Full retrieval path: cache + guardrail + retrieval +
   generation + feedback = 900 ms, 1.14 units.
2. Mixed traffic: time = 100 x 10 + 20 x 15 + 80 x 900
   = 1,000 + 300 + 72,000 = 73,300 ms. Cost = 100 x 0.02
   + 20 x 0.03 + 80 x 1.14 = 2.00 + 0.60 + 91.20 = 93.80 units.
   All-full traffic: time = 200 x 900 = 180,000 ms; cost
   = 200 x 1.14 = 228.00 units. Saved: 180,000 - 73,300
   = 106,700 ms, i.e. 106,700 / 180,000 = 59.3% faster; and
   228.00 - 93.80 = 134.20 units, i.e. 134.20 / 228.00 = 58.9%
   cheaper.
3. A blocked request walks cache check and guardrail check only —
   it never reaches retrieval, generation, or the feedback log,
   because the demo returns early on a block. The missing feedback
   entry means blocks leave no learning signal: the team cannot
   count, review, or tune what gets blocked from this log alone.
   (Logging blocks separately would be a sensible improvement.)
4. Advantage: repeat questions skip guardrails, retrieval, and
   generation entirely — the fastest possible path. Risk: a cached
   answer bypasses fresh guardrail checks, so if policy or facts
   change after caching, a stale or now-disallowed answer can be
   served without re-checking. Caches need expiry or invalidation
   for exactly this reason.
5. Users rate answers; ratings accumulate in the feedback log;
   retrieval then prefers the notes behind highly rated answers and
   demotes the notes behind poor ones. The signal flows from real
   use back into the system's choices, so answer quality improves
   from evidence instead of guesses.
