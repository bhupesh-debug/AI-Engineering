# Module 3 exercises — Prompt engineering and RAG

Work from README section 3, `src/rag.py`, `src/rag_eval.py`, and
`src/defense_taxonomy.py`. All documents and attacks are synthetic.

Recall the analogy: RAG is an open-book exam — look up the right
pages first, then answer with the book open.

## Problems

1. In `src/rag.py`, the query "what is LoRA fine tuning" retrieves
   which document first? What makes that document win: which shared
   words matter most, and why do rare words count more than common
   ones in TF-IDF?
2. Four queries have first-relevant-document ranks [1, 2, absent, 1]
   in the top 3. Compute hit rate @3 and MRR @3, showing the steps.
3. From `src/rag_eval.py`'s chunking comparison: (a) which chunk
   size wins the detail question on cosine score, and by how much?
   (b) For the spanning question with one chunk allowed, what
   fraction of the question does the best small chunk cover, and
   what fraction does the best large chunk cover?
4. Name the defense layer that catches indirect (retrieved-content)
   injection, and explain in one sentence why the user-input phrase
   scan cannot catch it.
5. RAG is said to reduce hallucinations. Explain the mechanism in
   two sentences, then name one way retrieval can still mislead an
   answer.
