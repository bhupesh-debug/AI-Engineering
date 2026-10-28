# Module 1 exercises — Foundations and post-training

Work from README section 1 and `src/lora.py`. All numbers are toy
numbers from the project, not real-model measurements.

Recall the analogy: the apprentice cook copies the master first
(SFT), then cooks while the master tastes and corrects (RL).

## Problems

1. In one or two sentences each, say what SFT does and what RL does,
   and why a team would use RL after SFT instead of SFT alone.
2. In `src/lora.py`, the frozen base matrix is 2 rows x 3 inputs and
   reads only the first two inputs. Which input can the base not
   handle, and what does the rank-1 adapter learn that fixes it?
3. A new task needs two independent directions of change. Can a
   rank-1 adapter solve it perfectly? Explain using the idea that
   an adapter's rank caps its directions.
4. Put these stages in order and say what each stage adds:
   (a) reinforcement learning, (b) pretraining, (c) supervised
   fine-tuning.
5. A teammate says "post-training is just more pretraining." Give
   two concrete differences between pretraining and post-training
   (data, objective, or outcome).
