# Module 4 exercises — Fine-tuning or RAG? The decision workflow

Work from README section 4 and `docs/decision-guide.md`. Every
scenario below is fictional; decide from the failure, not the fashion.

Recall the ladder: prompt + examples, then simple retrieval, then
complex retrieval OR fine-tuning, then combine both.

## Problems

1. A support bot must answer with today's refund policy, which
   changes every quarter. RAG or fine-tuning? Justify in one
   sentence using the ladder's logic.
2. A report generator must always answer in a fixed company format
   (heading, three bullets, disclaimer line), but its facts are
   stable. RAG or fine-tuning? Justify in one sentence.
3. A team fine-tuned a model, but answers still cite last year's
   prices. Which ladder step did they skip, and what should they
   add?
4. A team's retrieved passages are correct, but answers ignore the
   requested tone. Which rung is failing, and which rung fixes it?
5. From the decision guide's question table: a user asks, "Is the
   fact changing often (prices, policies, news)?" If the answer is
   yes, which side does the table lean toward, and why does
   changing data favor that side?
