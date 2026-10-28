# Decision guide: RAG or fine-tuning?

One-page companion to the AI Engineering learning project. This is a
conceptual ladder from the book's framework (as summarized), not a
vendor benchmark — no numbers here describe a real system. Start at
the top and climb only as far as the failure in front of you requires.

## The 4-step ladder

```
Step 1: Prompt + examples
   "Here is the task, and here are two good answers."
   Cost: nothing but words. Try this first, always.
   Move on when: answers are wrong in ways examples do not fix.

Step 2: Simple retrieval (RAG)
   Search your notes, add the best passages to the prompt, then answer.
   Fixes: missing facts, stale facts, made-up specifics.
   Move on when: the right passages are found but answers stay weak,
   or the needed behavior is a style/skill, not a fact.

Step 3: Complex retrieval OR fine-tuning — pick by what is failing
   - Complex retrieval when: the knowledge exists but is hard to find
     (better chunking, ranking, hybrid search, more sources).
   - Fine-tuning when: the model needs a new behavior, tone, format,
     or task skill that no retrieved passage can supply.
   Move on when: one side alone still leaves a gap the other side owns.

Step 4: Combine both
   Retrieval feeding a fine-tuned model. The fine-tuned model knows
   how to behave; retrieval keeps its facts fresh and specific.
```

## Questions that pick the rung

| Ask this | If yes, lean toward |
| --- | --- |
| Is the answer a fact that lives in my documents? | RAG |
| Is the fact changing often (prices, policies, news)? | RAG |
| Is the problem the model's tone, format, or task skill? | Fine-tuning |
| Do I need the same behavior on every request, with no documents? | Fine-tuning |
| Do I have labeled examples of good behavior? | Fine-tuning (they are its fuel) |
| Do I have documents but almost no labeled examples? | RAG |
| Is latency or cost per request the binding constraint? | RAG + caching first; LoRA keeps fine-tuning cheap |

## What each side cannot do

- **RAG cannot** teach a skill, fix a tone, or help when the documents
  do not contain the answer. It also adds a retrieval step that can
  fail on its own (wrong passage, missing passage).
- **Fine-tuning cannot** supply fresh facts, and its knowledge freezes
  at training time. It also costs training effort and labeled data,
  and a fine-tuned model can still hallucinate — confidence is not
  correctness.

## How to tell you picked wrong

- You built RAG and answers are fluent but stylistically wrong, or
  ignore your format every time: the gap is behavior, not knowledge —
  consider fine-tuning.
- You fine-tuned and answers are stylish but factually stale or
  invented: the gap is knowledge, not behavior — add retrieval.
- Either way, measure before and after with the evaluation tools
  (entropy/perplexity for model fit, a rubric judge with human spot
  checks for answer quality). A decision without a before-and-after
  measurement is a guess.

## Cheap fine-tuning note

When fine-tuning is the answer, LoRA is usually the first technique to
reach for: freeze the base weights, train small low-rank adapters, and
serve many adapters on one base model. See `src/lora.py` for the
parameter arithmetic. And when answers feel slow, check speculative
decoding (`src/speculative.py`) before buying bigger hardware — a
good draft model can cut waiting time without changing quality.
