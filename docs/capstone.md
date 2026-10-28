# Capstone — design an AI assistant for a fictional company

## The brief: Harborline Advisors (fictional)

Harborline Advisors is a fictional advisory firm. Its advisors
answer client questions about retirement planning, drawing on two
sources: (a) a library of plain-language guides that update every
year when tax and benefit rules change, and (b) the firm's own
house style for client letters (a fixed format: summary, three
findings, next steps, disclaimer). Clients ask in plain language,
often vaguely. The firm has three hard requirements:

1. Answers must cite the current year's guides, never last year's.
2. Every client letter must follow the house format exactly.
3. The system must never give personalized financial advice — it
   may explain concepts and show worked examples, but any request
   for a personal recommendation must be refused with a referral
   to a human advisor. Cost and latency matter: the firm serves
   many repeat questions.

Your design must apply all seven concepts from this project, with
trade-offs stated for each. All numbers in your design should come
from this project's toy models or be labeled as assumptions — do
not import vendor prices, real-model benchmarks, or real company
data. The company is fictional; nothing here describes a real firm.

## Sample solution (one good answer, not the only one)

1. Foundations and post-training: start from a general model,
   SFT on house-format letters (summary, three findings, next
   steps, disclaimer) so the format is learned behavior, then RL
   scored on format compliance and refusal correctness. Trade-off:
   training costs effort up front, but format compliance cannot be
   achieved by retrieval alone — no passage teaches a format.
2. Evaluation: track perplexity on held-out guide text as a
   fluency sanity check, but judge quality with a rubric judge
   (citation present? format followed? disclaimer present?) checked
   against human-graded samples. Guard the judge: strip length
   bonuses that reward padding, score answers individually (never
   pairwise by position), and hide authorship to limit
   self-enhancement bias. Trade-off: the judge is fast and cheap
   but inherits biases, so human grading of a sample never stops.
3. Prompt engineering and RAG: retrieve the current year's guide
   passages before answering, so requirement 1 is structural, not
   aspirational — last year's guides are removed from the index
   at each annual update. Chunk guides at sentence-to-paragraph
   size and retrieve top-k, so multi-fact questions recover split
   context. Trade-off: retrieval freshness beats retraining, but
   retrieval can still fetch the wrong passage, so answers cite
   their sources for checking.
4. Fine-tuning or RAG decision: this design uses step 4 of the
   ladder — combine both — deliberately: fine-tuning owns the
   format behavior, retrieval owns the facts. Either alone fails
   one of the first two requirements. Trade-off: two systems to
   maintain instead of one, justified because each requirement
   maps to a different rung.
5. LoRA: serve the house-format behavior as a LoRA adapter on a
   shared base model (rank chosen from the sweep's logic: enough
   directions for format + refusal behavior, no more), keeping one
   base for all firm tools. Trade-off: adapters are cheap to store
   and swap, but rank must match the behavior's true complexity —
   too small leaves format errors, too large wastes parameters.
6. Speculative decoding: enable it only if the draft model's
   measured accuracy clears the breakeven for the chosen draft
   length (about 0.287 at length 4 in the toy model); otherwise
   leave it off. Trade-off: real latency wins when the drafter is
   decent, real slowdowns when it is not — measure, don't assume.
7. Architecture: request → cache check → guardrail check →
   retrieval → generation → feedback log. Guardrails enforce
   requirement 3 (refuse personal recommendations with a human
   referral) and sit before retrieval, so refused requests never
   pay retrieval or generation costs. Cache serves repeat questions
   (the firm's most common ones) at about 1% of a full request's
   toy cost. Feedback ratings steer retrieval toward passages
   behind highly rated answers. Trade-off: cache-before-guardrail
   is fastest but risks serving a stale answer after policy
   changes — mitigate with cache expiry at each annual guide
   update. Economics from the toy model: a day of mixed traffic
   (40% cached, 5% blocked, 55% full) costs about 44% less time
   and money than all-full traffic.

## Grading rubric (100 points)

- Foundations/post-training (10): SFT and RL roles distinguished,
  order justified.
- Evaluation (15): perplexity's limits stated; rubric judge
  described; at least two biases named with mitigations.
- RAG (15): retrieval before answering; annual-update mechanism
  (old guides out of the index); chunking choice justified.
- Decision (10): ladder rung chosen from the failures, with the
  combine-both justification (or a defended alternative).
- LoRA (10): adapter role, rank reasoning, shared-base benefit.
- Speculative decoding (10): breakeven rule applied (measure
  before enabling), not assumed.
- Architecture (15): full route traced; guardrail placement
  justified; cache economics stated; feedback loop's effect named.
- Trade-offs and honesty (15): at least one real trade-off per
  concept; no invented vendor numbers, benchmarks, or real-company
  claims; toy numbers labeled as toy.

Score yourself: 90-100: capstone-ready — you can defend this design
in a review. 75-89: solid — revisit the rubric rows you missed and
rework those sections. 60-74: partial — redo the missed modules'
exercises first. Below 60: re-walk the curriculum before retrying
the capstone; the gaps are in the modules, not in this brief.
