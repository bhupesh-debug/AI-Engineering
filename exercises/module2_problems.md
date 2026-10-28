# Module 2 exercises — Evaluation methodology

Work from README section 2, `src/metrics.py`, and `src/judge.py`.
Show your arithmetic; all data is synthetic.

Recall the analogy: grading homework is slow when the teacher reads
every paper, so a star pupil grades instead — fast, but with habits
that bend the grades.

## Problems

1. Compute the entropy (in bits) of (a) a fair coin, probabilities
   [0.5, 0.5], and (b) a certain outcome, probabilities [1.0, 0.0].
   Use entropy = -sum(p * log2(p)), with 0 * log2(0) treated as 0.
2. Convert each entropy to perplexity with perplexity = 2^entropy.
   What does a perplexity of 1 mean in plain language?
3. The base demo's rubric: start at 1, add up to 3.5 for keyword
   coverage (4 keywords), add 0.5 if the answer exceeds 60 words,
   clamp to [1, 5]. Score (a) an answer covering 3 of 4 keywords
   in 30 words, and (b) an answer covering 2 of 4 keywords in
   70 words.
4. Judge scores are [5, 2, 4] and human scores are [5, 3, 4] for
   three answers. Compute the mean absolute error (MAE).
5. Perplexity measures how surprised a model is by text. Give one
   reason perplexity alone cannot certify that an answer is correct
   or useful, and name the evaluation tool from this module that
   covers that gap.
