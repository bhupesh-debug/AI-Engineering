# Curriculum — a learning path through AI Engineering

Follow the modules in order. Each module ends with a self-check:
you are done with a module only when you can pass its check without
looking anything up. Times are honest estimates for reading, running
the demos, and doing the exercises — not for skimming.

## Module 1 — Foundations and post-training (about 30 minutes)

- Read: README section 1.
- Run: `python src/lora.py` (the shaping idea, made concrete).
- Do: `exercises/module1_problems.md`, then check against
  `exercises/module1_solutions.md`.
- Prerequisite: none.
- Learning objective: explain, in plain language, what pretraining,
  SFT, and RL each add, and why they run in that order.
- Done looks like: you can say why RL follows SFT (not the reverse)
  and which input the base demo's adapter had to learn.

## Module 2 — Evaluation methodology (about 45 minutes)

- Read: README section 2.
- Run: `python src/metrics.py`, `python src/judge.py`,
  `python src/judge_biases.py`.
- Do: `exercises/module2_problems.md`.
- Prerequisite: Module 1 (you need to know what is being shaped
  before you can judge whether the shaping worked).
- Learning objective: compute entropy and perplexity by hand,
  score an answer with the demo rubric, and name one judge bias
  with its mitigation.
- Done looks like: you can score a new answer with the rubric and
  explain why perplexity alone cannot certify correctness.

## Module 3 — Prompt engineering and RAG (about 60 minutes)

- Read: README section 3.
- Run: `python src/rag.py`, `python src/rag_eval.py`,
  `python src/defense.py`, `python src/defense_taxonomy.py`.
- Do: `exercises/module3_problems.md`.
- Prerequisite: Module 2 (retrieval quality is measured with the
  evaluation tools: hit rate, MRR).
- Learning objective: trace a question through retrieve-rank-answer,
  read a hit-rate/MRR report, state the chunking trade-off, and map
  each attack type to the layer that stops it.
- Done looks like: you can explain why small chunks win on
  precision but lose on single-chunk coverage, and why a phrase scan
  cannot stop indirect injection.

## Module 4 — Fine-tuning or RAG? (about 30 minutes)

- Read: README section 4 and `docs/decision-guide.md`.
- Run: none new — this module is judgment, practiced on scenarios.
- Do: `exercises/module4_problems.md`.
- Prerequisite: Module 3 (you cannot choose between retrieval and
  fine-tuning before you understand what retrieval does).
- Learning objective: given a failure description, pick the correct
  ladder rung and justify it from the failure, not from fashion.
- Done looks like: you answer "changing facts" with RAG and "fixed
  format" with fine-tuning without hesitating, and you know what
  "combine both" is for.

## Module 5 — LoRA (about 60 minutes)

- Read: README section 5.
- Run: `python src/lora.py`, `python src/lora_sweep.py`.
- Do: `exercises/module5_problems.md`.
- Prerequisite: Modules 1 and 4 (LoRA is fine-tuning, so it needs
  the post-training idea and the decision context for when
  fine-tuning is the right rung at all).
- Learning objective: compute LoRA parameter counts for any layer
  and rank, read the rank sweep as diminishing returns, and explain
  the symmetry trap.
- Done looks like: you can price rank 8 on a 256x256 layer from
  memory of the formula (not the answer) and say why rank 1 cannot
  solve a 3-direction task.

## Module 6 — Speculative decoding (about 45 minutes)

- Read: README section 6.
- Run: `python src/speculative.py`, `python src/spec_curve.py`.
- Do: `exercises/module6_problems.md`.
- Prerequisite: Module 1 (you need the generation loop — one token
  at a time — before a technique that accelerates it makes sense).
- Learning objective: compute expected tokens per step from draft
  accuracy, read a speedup curve, and state the breakeven rule.
- Done looks like: you can explain why a longer draft needs a more
  accurate drafter, and why accuracy 0.0 makes speculation slower
  than one-by-one generation.

## Module 7 — Architecture (about 60 minutes)

- Read: README section 7.
- Run: `python src/pipeline.py`, `python src/pipeline_econ.py`.
- Do: `exercises/module7_problems.md`.
- Prerequisite: Modules 1-6 (the blueprint assembles everything:
  retrieval, guardrails, generation speed, evaluation, and cost).
- Learning objective: trace any request through the pipeline,
  price each route, and explain what the feedback loop changes.
- Done looks like: you can price a day of mixed traffic from the
  stage costs and name the cache-order trade-off (speed versus
  stale-policy risk).

## After all modules

- Take `quizzes/quiz.md` (35 questions). Use its scoring guide to
  find modules to revisit — a low module score means redo that
  module's exercises, not re-read everything.
- Finish with `docs/capstone.md`: design a full system for a
  fictional company, applying all seven concepts, then grade
  yourself against its rubric.

Total path: about 5.5 hours of modules, plus 45 minutes for the quiz
and 1-2 hours for the capstone. The demos are the spine: if you only
read, you have toured the ideas; if you run, exercise, and assess,
you own them.
