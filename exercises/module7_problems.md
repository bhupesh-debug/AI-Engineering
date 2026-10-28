# Module 7 exercises — Architecture: the blueprint

Work from README section 7, `src/pipeline.py`, and
`src/pipeline_econ.py`. Stage costs are toy units, labeled as such
in the demo — the comparison shape is the lesson, not the currency.

Recall the analogy: a good school library checks the pinned board
(cache) first, checks the question is allowed (guardrails), fetches
books (retrieval), writes the answer, and pins up a "did this help?"
slip (feedback).

## Problems

1. List the stages each route walks and its (time, cost) from the
   demo: (a) cache hit, (b) blocked, (c) full retrieval path.
2. A day brings 200 requests: 100 cache hits, 20 blocked, 80 full
   retrievals. Compute total time and total cost, then compute the
   totals if all 200 went through the full path, and the percentage
   saved on each.
3. In `src/pipeline.py`, a blocked request returns before the
   feedback log is appended. Which stages does it walk, and what
   does the missing feedback entry mean for learning from blocks?
4. The pipeline checks the cache before the guardrails. Name one
   advantage of that order and one risk (think about what changes
   after an answer is cached).
5. Feedback ratings are supposed to steer future retrieval toward
   better notes. Describe the loop in two sentences: what signal
   flows where, and what changes as a result?
