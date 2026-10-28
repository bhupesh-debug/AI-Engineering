# AI Engineering: Building Applications with Foundation Models

A plain-language learning project built from the concepts in Chip Huyen's
book *AI Engineering: Building Applications with Foundation Models*, as
presented in a video summary by Aayush. Every hard idea below gets a
plain-language explanation with an everyday analogy, plus a visual. Every
demo is small, runnable, and uses only synthetic toy data.

## Scope note — read this first, it is the honest part

- This project is built from the **provided summary** of the book, not
  from the book's text. There are no quotations from the book here, no
  page numbers, and no video links.
- The book itself contains no code. **All code in this project is
  original, illustrative implementation of the concepts**, written to
  make the ideas runnable — it is not the book's code and not a
  reproduction of any real system.
- No API keys, no external model calls, no real company data, no
  claimed benchmarks. Every dataset is synthetic or toy and labeled as
  such. If a number looks precise, it is a worked toy example, not a
  measurement of a real model.
- Audience, as the summary frames it: data scientists, product
  managers, and team leaders who want intuition and trade-off sense for
  real-world AI systems — breadth first, with enough depth to start
  from.

## Concept map

```
Foundations: a language model predicts text...
      |
      v
Post-training (SFT + RL) shapes it into a helper...
      |
      +--> How do we know it works?  EVALUATION (entropy, perplexity, AI as a Judge)
      |
      +--> How do we make it answer well?  PROMPTS + RAG (or fine-tuning?)
      |
      +--> How do we make it cheap and fast?  LoRA + SPECULATIVE DECODING
      |
      v
ARCHITECTURE: guardrails + cache + feedback hold the whole system together
```

## 1. Foundations and post-training

**Plain-language explanation.** A language model starts life as a
prediction machine: given some words, guess the next one. That alone is
not an assistant. AI engineering is the work of turning that prediction
machine into a system that answers questions, follows instructions, and
behaves reliably. Post-training is the shaping stage, and it has two
main tools.

- **Supervised fine-tuning (SFT):** show the model many examples of
  good behavior — a question, then the kind of answer you want — and
  train it to imitate them.
- **Reinforcement learning (RL):** let the model produce answers, score
  them, and steer it toward the answers that score well.

**Everyday analogy.** Think of an apprentice cook. First the apprentice
watches the master and copies each dish exactly — that is SFT. Then the
apprentice cooks alone while the master tastes every plate, praising
the good ones and correcting the bad — that is RL. Copying teaches the
moves; tasting teaches the judgment.

**Visual — the shaping pipeline:**

```
raw text
   |
   v
[ predict the next word ]  <- pretraining: learns language
   |
   v
[ copy good examples ]     <- SFT: learns the desired behavior
   |
   v
[ get scored, improve ]    <- RL: learns from feedback
   |
   v
deployed assistant (inside a system — see concept 7)
```

**Try it:** the shaping idea shows up concretely in `src/lora.py`,
where a frozen base plus a trained adapter learns a task the base
cannot do alone.

## 2. Evaluation methodology

**Plain-language explanation.** You cannot improve what you cannot
measure, and "it feels good" is not a measurement. Two classic meters
come from information theory:

- **Entropy** measures surprise. A distribution spread evenly across
  many options has high entropy; one concentrated on a single option
  has entropy near zero.
- **Perplexity** is entropy turned into a head-count: 2 raised to the
  entropy. A perplexity of 4 means the model is about as uncertain as
  if it were choosing between 4 equally likely options.

**Everyday analogy.** Imagine a bag of marbles. A bag of only red
marbles never surprises you — entropy 0, perplexity 1. A bag split
evenly between red and blue is a coin flip every time — entropy 1 bit,
perplexity 2. Perplexity is just a way of saying "how many marbles
could this plausibly be?"

**Visual — surprise grows with options:**

```
certain (1 option):   |#|                     perplexity  1
coin flip (2 options):|##########|            perplexity  2
four-way split:       |####################|  perplexity  4
```

**AI as a Judge.** Human grading is slow and expensive, so teams use a
strong model as the grader: it scores or critiques another model's
outputs against a rubric. That buys speed and scale, but it imports
three problems you must measure, not assume away: picking a judge
capable of nuanced evaluation, the cost-versus-accuracy trade-off of
running a strong judge, and the judge's own biases — for example,
preferring longer answers even when the content is no better. The
demo catches exactly that bias in the act.

**Visual — the judge loop:**

```
model output ──> [ judge model + rubric ] ──> score + critique
                      ^                              |
                      |                              v
                 judge selection,              iterate on the
                 cost, and bias checks          system, not the score
```

**Try it:**

```
python3 src/metrics.py   # entropy + perplexity on a toy corpus
python3 src/judge.py     # rubric judge vs human labels + bias demo
```

## 3. Prompt engineering and RAG

**Plain-language explanation — defensive prompting.** A prompt is an
instruction, and user input is data. Trouble starts when the model
cannot tell the two apart: a user writes "ignore your instructions and
do this instead," and a careless setup obeys the scribble instead of
the sheet. Defensive prompt engineering is the discipline of keeping
that hierarchy straight: system instructions outrank everything, user
input is wrapped and treated as data, and known override phrases are
caught and refused.

**Everyday analogy.** A teacher hands out a worksheet and says, "Only
follow what is printed on this sheet." A prankster writes in the
margin, "Ignore the sheet, give me the answers." A defended classroom
is one where margin writing is always treated as scribble, never as
new instructions — and where the teacher knows the common pranks by
heart.

**Visual — who outranks whom:**

```
SYSTEM instructions      (highest priority — the sheet)
   |
USER input as data       (wrapped in delimiters — the margin)
   |
MODEL output             (follows the sheet, never the margin)
```

**Plain-language explanation — RAG.** Retrieval-Augmented Generation
gives the model external context at answer time: before answering, the
system searches a knowledge base for the most relevant passages and
adds them to the prompt. That reduces made-up answers (hallucinations)
and supplies up-to-date, specific facts without retraining anything.

**Everyday analogy.** RAG is an open-book exam. Instead of forcing the
student to memorize every textbook, you let them look up the right
pages first and answer with the book open. The lookup itself is just
careful word matching: rare, distinctive words count more than common
ones.

**Visual — the RAG flow:**

```
question ──> [ search the notes ] ──> best passages
                                        |
question + passages ──> [ model ] ──> answer grounded in the notes
```

**Try it:**

```
python3 src/defense.py   # 8 injection attempts vs undefended/defended
python3 src/rag.py       # TF-IDF retrieval + labeled stub answer
```

## 4. Fine-tuning or RAG? The decision workflow

**Plain-language explanation.** Fine-tuning changes the model's
internal weights by training it on your data, so its behavior, style,
or task skill shifts permanently. RAG leaves the weights alone and
instead hands the model better context at answer time. The book's
decision workflow is a ladder — climb only as far as you must:

1. Start with a prompt, including examples.
2. If that is not enough, add simple retrieval (RAG).
3. If still not enough, choose between complex retrieval and
   fine-tuning, based on what is actually failing.
4. You can combine both: retrieval feeding a fine-tuned model.

**Everyday analogy.** You are teaching someone to cook your family
recipes. First you just tell them the recipe (prompt). If they keep
forgetting ingredients, you pin the recipe card on the fridge (RAG).
If their technique itself is wrong, you send them to cooking school
(fine-tuning). And nothing stops you from doing both: trained cook,
recipe card still on the fridge.

**Visual — the ladder (full guide in `docs/decision-guide.md`):**

```
start: prompt + examples
   |  not enough?
   v
simple RAG
   |  still not enough?
   v
complex retrieval  OR  fine-tuning   (pick by what is failing)
   |
   v
combine: RAG + fine-tuned model
```

**Try it:** `python3 src/rag.py` for the retrieval rung and
`python3 src/lora.py` for the fine-tuning rung — then read
`docs/decision-guide.md` for the one-page version of this ladder.

## 5. LoRA — fine-tuning on a budget

**Plain-language explanation.** Full fine-tuning updates every weight
in a huge model — billions of numbers, expensive to store and serve.
LoRA (Low-Rank Adaptation) freezes all of those weights and trains only
two small matrices whose product is the update. If the base layer is
512 by 512, a rank-4 adapter needs 4 × (512 + 512) = 4,096 trainable
numbers instead of 262,144 — and because the update is built as a
product of a tall-thin matrix and a short-wide one, its rank can never
exceed the small inner size. One frozen base model can then host a
different cheap adapter for every task.

**Everyday analogy.** A giant statue stands frozen in the square — you
may not re-carve it. But you may attach small clay patches, one per
occasion: a hat for the festival, a scarf for winter. Each patch is
tiny compared to the statue, easy to swap, and the statue itself never
changes.

**Visual — the shapes:**

```
base weights W (frozen)        adapter update = B x A (trained)
┌──────────────┐               ┌──┐   ┌──────────┐   ┌──────────┐
│              │               │B │   │          │   │          │
│   512 x 512  │      +        │  │ x │    A     │ = │  update  │
│              │               │  │   │  rank 4  │   │  rank ≤4 │
└──────────────┘               └──┘   └──────────┘   └──────────┘
trainable: 262,144              trainable: 4,096
```

**Try it:**

```
python3 src/lora.py    # parameter math + a rank-1 adapter that learns
```

## 6. Speculative decoding — faster answers, same quality

**Plain-language explanation.** A generating model normally writes one
word at a time, each word waiting on the last — a slow chain. In
speculative decoding, a small, fast draft model scribbles several
candidate words ahead. The big model then checks the whole batch at
once, in parallel, and keeps the longest run it agrees with, plus one
corrected word of its own. When the draft is usually right, several
approved words come out per round instead of one, and waiting time
drops. When the draft is usually wrong, the checking costs more than
it saves — the demo shows that honest edge too.

**Everyday analogy.** A fast junior assistant drafts a paragraph while
the senior editor reads it in one pass, crossing out from the first
mistake onward. The team still produces several approved sentences per
round — as long as the junior is usually right. A junior who is
usually wrong just creates extra reading for the editor.

**Visual — one round:**

```
draft model (fast):   proposes:  w1  w2  w3  w4
big model (checks):  agrees:     w1  w2  ✗
output this round:   w1  w2  +  corrected word
                     └─ kept ─┘  └─ verifier's own ─┘
```

**Try it:**

```
python3 src/speculative.py   # tokens/step and speedup vs draft accuracy
```

## 7. Architecture — the blueprint that holds it together

**Plain-language explanation.** A real AI application is not a model;
it is a system around a model. The book's blueprint has three load-
bearing parts. **Guardrails** decide what is allowed in and out —
blocking disallowed requests before they reach the model and checking
answers before they reach the user. **Caching** remembers answers to
repeated questions so the system can reuse them instantly instead of
paying for retrieval and generation again. **User feedback loops**
record how people react to answers, and that record feeds back into
which notes retrieval prefers and where the system is failing.

**Everyday analogy.** A good school library works this way. A student
asks a question. First the librarian checks whether the same question
was already answered and pinned to the board (cache). Then the
librarian checks the question is allowed (guardrails). Then they fetch
the right books (retrieval), write the answer, and pin a slip next to
it saying "tell us if this helped" (feedback) — and those slips decide
which books get fetched next time.

**Visual — the pipeline:**

```
request ──> cache? ──(hit)──> answer
               |
             (miss)
               v
          guardrail? ──(block)──> refusal
               |
             (pass)
               v
          retrieval ──> answer assembly ──> feedback log
                                                     |
                                              (feeds back into
                                               retrieval choices)
```

**Try it:**

```
python3 src/pipeline.py   # cache hit, guardrail block, feedback log
```

## How to run everything

```bash
cd ai-engineering
python3 src/metrics.py       # entropy + perplexity
python3 src/rag.py           # TF-IDF retrieval + stub answer
python3 src/lora.py          # LoRA parameter math + trained adapter
python3 src/speculative.py   # speculative decoding simulation
python3 src/judge.py         # AI-as-judge rubric + verbosity bias
python3 src/defense.py       # defensive prompting, undefended vs defended
python3 src/pipeline.py      # cache + guardrails + retrieval + feedback
python3 -m pytest tests/ -q  # full test suite (35 tests)
```

Requirements: Python 3.10 or newer. `numpy` is listed in
`requirements.txt` but is optional — every demo falls back to pure
Python when it is absent, and the toy training numbers are identical
either way. `pytest` is needed only to run the tests.

## Project layout

```
README.md                  this guide
docs/decision-guide.md     RAG vs fine-tuning, one page
src/
  metrics.py               entropy + perplexity
  rag.py                   TF-IDF retrieval + stub answer
  lora.py                  LoRA math + tiny trained adapter
  speculative.py           speculative decoding simulation
  judge.py                 rubric judge + bias demo
  defense.py               defensive prompting demo
  pipeline.py              cache + guardrails + retrieval + feedback
tests/                     pytest tests, one file per demo
requirements.txt           numpy (optional at runtime), pytest
LICENSE                    MIT
```

## Limitations, stated plainly

- Everything here is a teaching model of the concepts, not a
  production component. The retrieval is keyword TF-IDF, not semantic
  search; the judge is a transparent rubric, not a model; the defense
  is a phrase list, not a security boundary; the pipeline's answers
  are template assemblies, not generated text.
- No numbers in this project describe any real model, product, or
  benchmark. Where the summary gave a concept without numbers, this
  project invents only clearly labeled toy numbers to make the concept
  runnable.
- If you take any idea from here into a real system, validate it
  against real data, real users, and real threat models first. The
  book's value, as the summary presents it, is breadth and trade-off
  intuition — this project is a starting point in exactly that sense.
