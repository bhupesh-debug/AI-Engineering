# Module 5 solutions — LoRA: fine-tuning on a budget

1. Full fine-tuning = 512 x 512 = 262,144 parameters. LoRA
   = rank x (in + out) = 4 x (512 + 512) = 4,096 parameters.
   Saved = 1 - 4096/262144 = 1 - 0.015625 = 0.984375, i.e. 98.4%.
2. Full = 256 x 256 = 65,536. LoRA = 8 x (256 + 256) = 4,096.
   Saved = 1 - 4096/65536 = 1 - 0.0625 = 0.9375, i.e. 93.75%.
   (Note the coincidence: rank 8 on a 256x256 layer costs the same
   4,096 parameters as rank 4 on a 512x512 layer.)
3. Rank 2 captures 59.04% of the spectrum's energy, leaving
   40.96% residual. Rank 8 captures 97.19%, leaving 2.81%.
   Doubling rank from 2 to 8 buys about 38 points of captured
   energy; the next doubling (to 16) buys under 3 points — the
   diminishing-returns shape of the whole trade-off.
4. A rank-1 update spans exactly one direction, but this task's
   needed change has three independent directions (rank 3). Rank 1
   captures only the dominant direction, so 0.1479 of loss remains
   no matter how long it trains. Rank 3 spans all three directions,
   so it can represent the needed change exactly and reach 0.0000.
5. With all-equal starts, every rank component begins identical,
   receives identical gradients, and stays identical through
   training — the adapter behaves as rank 1 regardless of its
   nominal rank. Varied starting values break the symmetry so each
   component can learn a different direction.
