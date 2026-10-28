# Module 6 exercises — Speculative decoding

Work from README section 6, `src/speculative.py`, and
`src/spec_curve.py`. All numbers come from the simulation's cost
model (one large-model step = 1.0 unit, one draft token = 0.1 unit).

Recall the analogy: a fast junior drafts, a senior editor checks a
whole batch at once and keeps everything before the first mistake.

## Problems

1. Expected tokens per step = 1 + a + a^2 + ... + a^k. Compute it
   for draft accuracy a = 0.8 and draft length k = 4. Show the terms.
2. Using your answer to problem 1 and a per-step cost of 1.4 units
   (4 draft tokens x 0.1 + 1.0 verification), compute the speedup
   versus one-by-one generation.
3. The curve reports breakeven draft accuracies of about 0.287 for
   draft length 4 and about 0.445 for draft length 8. In plain
   language, why does the longer draft need a more accurate
   drafter to break even?
4. At draft accuracy 0.0 with draft length 4, the speedup is 0.714.
   Explain why it is below 1.0 — what is being paid for, and what
   is being produced?
5. Why does the formula add 1 to the accepted prefix length? What
   is that extra token, physically, in the verifier's step?
