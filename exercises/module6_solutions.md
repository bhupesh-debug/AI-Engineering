# Module 6 solutions — Speculative decoding

1. Expected tokens = 1 + 0.8 + 0.8^2 + 0.8^3 + 0.8^4
   = 1 + 0.8 + 0.64 + 0.512 + 0.4096 = 3.3616, about 3.362.
   Each term is the probability that the accepted prefix reaches
   that far; the leading 1 is the verifier's own token.
2. Speedup = tokens per step / cost per step = 3.3616 / 1.4
   = 2.401 (theory). The simulation at 20,000 steps reports 2.413
   — the small gap is simulation noise around the same value.
3. A longer draft costs more per round: 8 x 0.1 + 1.0 = 1.8 units
   versus 4 x 0.1 + 1.0 = 1.4 units. To break even, the round must
   produce more accepted tokens to cover the higher drafting bill,
   which requires a more accurate drafter — hence 0.445 versus
   0.287. Longer drafts raise both the ceiling and the entry fee.
4. At accuracy 0.0, every drafted token is rejected, so the round
   produces only the verifier's 1 correction token — but still pays
   0.4 units drafting plus 1.0 verifying, 1.4 units total, against
   1.0 unit for writing that token directly. 1.0 / 1.4 = 0.714:
   slower than one-by-one, because the drafting work is pure waste.
5. The +1 is the verifier's correction token. After the accepted
   prefix, the verifier always writes the token that should have
   come next at the first mismatch (or after a fully accepted
   draft). So every round yields at least one token, even when the
   draft is entirely wrong — which is also why the floor speedup
   at accuracy 0.0 is 1/cost rather than zero.
