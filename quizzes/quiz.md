# Self-assessment quiz — AI Engineering learning project

35 multiple-choice questions, 5 per module. Answer from the
project's own material (README, demos, decision guide). All numbers
are the project's toy numbers, not real-model measurements. Do not
peek at the key until you have answered all 35.

## Module 1 — Foundations and post-training

1. Supervised fine-tuning teaches a model mainly by:
   A. Scoring its outputs and steering toward high scores
   B. Copying good examples of desired behavior
   C. Retrieving passages at answer time
   D. Drafting tokens for a larger model to check
2. Reinforcement learning differs from SFT in that it:
   A. Uses no training data at all
   B. Learns from scored outputs rather than copied examples
   C. Freezes the model's weights
   D. Needs no example answers
3. In `src/lora.py`, the frozen base matrix reads inputs 1 and 2.
   Which input can it not handle?
   A. Input 1
   B. Input 2
   C. Input 3
   D. None — it handles all three
4. The correct post-training order is:
   A. RL, then SFT, then pretraining
   B. Pretraining, then SFT, then RL
   C. SFT, then pretraining, then RL
   D. Pretraining, then RL, then SFT
5. Post-training's job, in one line, is to:
   A. Teach language from raw text
   B. Turn a text predictor into a behaving assistant
   C. Speed up token generation
   D. Retrieve documents before answering

## Module 2 — Evaluation methodology

6. The entropy of a fair coin, probabilities [0.5, 0.5], is:
   A. 0 bits
   B. 0.5 bits
   C. 1 bit
   D. 2 bits
7. An entropy of 2 bits corresponds to a perplexity of:
   A. 2
   B. 4
   C. 8
   D. 16
8. Under the base demo's rubric, an answer covering all 4 keywords
   in 30 words scores:
   A. 3.5
   B. 4.0
   C. 4.5
   D. 5.0
9. Under the same rubric, an answer covering 0 keywords in 100 words
   scores:
   A. 1.0
   B. 1.5
   C. 2.0
   D. 2.5
10. Judge scores [4, 4] against human scores [5, 3] give an MAE of:
    A. 0.5
    B. 1.0
    C. 1.5
    D. 2.0

## Module 3 — Prompt engineering and RAG

11. RAG's first step at answer time is to:
    A. Fine-tune the model
    B. Retrieve passages related to the question
    C. Score the previous answer
    D. Draft tokens for verification
12. In `src/rag.py`, the query "what is LoRA fine tuning"
    retrieves which document first?
    A. Defensive prompt engineering
    B. LoRA fine-tuning
    C. Caching answers
    D. AI as a Judge
13. Four queries with first-relevant ranks [1, 2, absent, 1] in the
    top 3 have a hit rate @3 of:
    A. 0.50
    B. 0.625
    C. 0.75
    D. 1.00
14. Indirect injection arrives hidden inside:
    A. The user's own words
    B. Retrieved content
    C. The system prompt
    D. The cache
15. Small chunks beat large chunks mainly on:
    A. Coverage of multi-fact questions
    B. Precision for single-detail questions
    C. Cost per request
    D. Generation speed

## Module 4 — Fine-tuning or RAG?

16. A bot must answer with prices that change daily. Prefer:
    A. Fine-tuning
    B. RAG
    C. Reinforcement learning
    D. Speculative decoding
17. A generator must always emit a fixed report format, with stable
    facts. Prefer:
    A. RAG
    B. Fine-tuning
    C. Caching
    D. AI as a Judge
18. The decision ladder's first step is always:
    A. Simple retrieval
    B. Prompt + examples
    C. Fine-tuning
    D. Combine both
19. Retrieved facts are right but the tone is wrong. What is needed?
    A. Better retrieval
    B. Fine-tuning
    C. A bigger cache
    D. Faster decoding
20. The ladder's final step, "combine both," means:
    A. RAG feeding a fine-tuned model
    B. Two retrievers voting
    C. Two judges averaging
    D. Prompt plus cache

## Module 5 — LoRA

21. LoRA freezes:
    A. The adapter matrices
    B. The base model's weights
    C. The prompts
    D. The training data
22. A 512x512 toy layer at rank 4 trains how many LoRA parameters?
    A. 1,024
    B. 2,048
    C. 4,096
    D. 8,192
23. In the rank sweep's analytic table, rank 8 captures what share
    of the spectrum's energy?
    A. 59.04%
    B. 83.22%
    C. 97.19%
    D. 100.00%
24. On the sweep's trained 3-direction task, rank 3's final loss is:
    A. 0.1479
    B. 0.0417
    C. 0.0000
    D. 0.5000
25. Starting all adapter components from identical values causes:
    A. Faster training
    B. The symmetry trap (components stay identical)
    C. Overfitting
    D. Higher effective rank

## Module 6 — Speculative decoding

26. The leading 1 in "1 + a + a^2 + ..." is:
    A. The draft model's tokens
    B. The verifier's own correction token
    C. A cache hit
    D. The prompt tokens
27. With draft accuracy 0.8 and draft length 4, expected tokens per
    step are about:
    A. 2.36
    B. 3.36
    C. 4.10
    D. 5.00
28. The breakeven draft accuracy at draft length 4 is about:
    A. 0.10
    B. 0.287
    C. 0.445
    D. 0.80
29. At draft length 8, the breakeven accuracy compared with length 4
    is:
    A. Lower
    B. The same
    C. Higher
    D. Zero
30. At draft accuracy 0.0 and draft length 4, the speedup is:
    A. 0
    B. 0.714
    C. 1.0
    D. 1.4

## Module 7 — Architecture

31. The pipeline checks first:
    A. Guardrails
    B. The cache
    C. Retrieval
    D. Feedback
32. A cache-hit request costs how much time in the toy model?
    A. 900 ms
    B. 15 ms
    C. 10 ms
    D. 800 ms
33. A blocked request walks which stages?
    A. All five stages
    B. Cache check + guardrail check
    C. Cache check only
    D. Guardrail check only
34. Mixed traffic of 100 requests (40 cached, 5 blocked, 55 full)
    saves about how much time versus all-full traffic?
    A. 10%
    B. 44.5%
    C. 59%
    D. 90%
35. The feedback loop mainly steers:
    A. Guardrail rules
    B. Future retrieval choices
    C. Draft-model accuracy
    D. Adapter rank

## Answer key

1-B, 2-B, 3-C, 4-B, 5-B,
6-C, 7-B, 8-C, 9-B, 10-B,
11-B, 12-B, 13-C, 14-B, 15-B,
16-B, 17-B, 18-B, 19-B, 20-A,
21-B, 22-C, 23-C, 24-C, 25-B,
26-B, 27-B, 28-B, 29-C, 30-B,
31-B, 32-C, 33-B, 34-B, 35-B.

Worked checks for the numerical keys: Q8: 1 + 3.5 x (4/4) = 4.5,
no length bonus under 60 words. Q9: 1 + 0 + 0.5 = 1.5. Q10:
(|4-5| + |4-3|)/2 = 1.0. Q13: 3 hits / 4 = 0.75. Q22:
4 x (512 + 512) = 4,096. Q27: 1 + 0.8 + 0.64 + 0.512 + 0.4096
= 3.3616. Q30: 1.0 / 1.4 = 0.714. Q34: (90,000 - 49,975) /
90,000 = 44.5%.

## Scoring guide

- 32-35: Mastery. You can explain each concept, run its demo, and
  defend its trade-offs. Go to the capstone.
- 27-31: Strong. Revisit the exercises for each module where you
  missed more than one question, then re-take those five.
- 21-26: Working. Re-run the demos for your missed modules and redo
  their exercises before moving on — the gaps are usually one
  misunderstood mechanism, not general difficulty.
- 14-20: Shaky. Re-read the README sections for your missed modules
  and redo their exercises from scratch; do not skip the demos.
- 0-13: Restart. Follow `docs/curriculum.md` in order, running each
  demo as you reach it. The quiz will still be here afterwards.
