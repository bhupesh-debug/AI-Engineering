# Module 5 exercises — LoRA: fine-tuning on a budget

Work from README section 5, `src/lora.py`, and `src/lora_sweep.py`.
All dimensions are toy sizes, not any real model's dimensions.

Recall the analogy: the base model is a frozen statue; adapters are
small clay patches, one per job, on the shared statue.

## Problems

1. For a 512x512 toy layer at rank 4, compute full fine-tuning
   parameters, LoRA parameters, and the percentage saved. Show the
   formulas, not just the answers.
2. For a 256x256 toy layer at rank 8, compute the same three numbers.
3. From the rank sweep's analytic table (spectrum of 32 directions,
   importance decaying by 0.8): what fraction of energy does rank 2
   capture, and what fraction remains as residual? What about rank 8?
4. The trained check on the 3-direction task reports final losses
   0.1479 (rank 1), 0.0417 (rank 2), and 0.0000 (rank 3). Why can
   rank 1 not reach zero on this task, while rank 3 can?
5. In the sweep code, adapter matrices start from varied values,
   not all-equal values. Explain the failure that all-equal starts
   cause, in one or two sentences (the symmetry trap).
