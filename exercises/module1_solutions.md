# Module 1 solutions — Foundations and post-training

1. SFT (supervised fine-tuning) trains the model to imitate good
   examples: question in, desired answer out, repeated until the
   behavior sticks. RL (reinforcement learning) scores the model's
   own answers and steers it toward high-scoring ones. RL comes
   after SFT because SFT first gives the model a sensible behavior
   to refine — RL without that starting shape would be scoring
   noise — and because copying alone also copies the examples'
   flaws, while scoring can correct toward outcomes.
2. The base cannot handle input 3: its two rows read inputs 1 and
   2 only. The rank-1 adapter learns exactly the missing direction:
   when input 3 is on, add [1, 1] to the output (the training pair
   ([0, 0, 1], [1, 1]) proves it). The update is a 2x1 column times
   a 1x3 row, so its rank is 1 by construction.
3. No. An adapter's rank is the number of independent directions
   its update can express. A rank-1 update spans one direction, so
   a task needing two independent directions always leaves part of
   the change unlearned — the sweep's trained check shows this
   concretely (rank 1 leaves loss 0.1479 on a 3-direction task).
4. Order: (b) pretraining, then (c) SFT, then (a) RL. Pretraining
   adds general language ability by predicting the next word over
   raw text. SFT adds desired behavior by copying curated examples.
   RL adds judgment by scoring outputs and steering toward the
   ones that score well.
5. Any two of: pretraining trains on raw, unlabelled text while
   post-training trains on curated examples and scored outputs;
   pretraining's objective is next-word prediction while
   post-training's objective is behaving helpfully and safely;
   pretraining produces a general predictor while post-training
   produces an assistant. (Cost and data size also differ, but the
   objective/data distinction is the core.)
