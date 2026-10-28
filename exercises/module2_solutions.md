# Module 2 solutions — Evaluation methodology

1. (a) Entropy = -[0.5 * log2(0.5) + 0.5 * log2(0.5)]
   = -[0.5 * (-1) + 0.5 * (-1)] = 1 bit. A fair coin surprises
   you by exactly 1 bit per flip.
   (b) Entropy = -[1.0 * log2(1.0) + 0] = -[0] = 0 bits. A certain
   outcome carries no surprise at all.
2. Perplexity = 2^entropy. (a) 2^1 = 2. (b) 2^0 = 1. A perplexity of
   1 means the model is perfectly certain — as if choosing among
   exactly one option, with no uncertainty left.
3. (a) 1 + 3.5 * (3/4) + 0 = 1 + 2.625 = 3.625. The answer is under
   60 words, so no length bonus.
   (b) 1 + 3.5 * (2/4) + 0.5 = 1 + 1.75 + 0.5 = 3.25. The 70-word
   answer earns the 0.5 length bonus.
4. MAE = (|5 - 5| + |2 - 3| + |4 - 4|) / 3 = (0 + 1 + 0) / 3
   = 1/3, about 0.333. On average the judge is a third of a point
   away from the human label on this set.
5. Perplexity measures surprise (fluency), not truth: a smooth,
   confident, factually wrong answer can have low perplexity. The
   gap is covered by judging output quality against a rubric —
   AI as a Judge — calibrated against human labels.
