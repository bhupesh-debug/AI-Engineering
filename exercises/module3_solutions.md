# Module 3 solutions — Prompt engineering and RAG

1. The top document is "LoRA fine-tuning". The query's content
   words are lora, fine, tuning; all three appear in that note and
   in no other note, so its cosine similarity is highest. Rare
   words count more because TF-IDF weights a word by how few
   documents contain it: "lora" appears in one of six notes (high
   weight), while a word appearing everywhere would carry almost
   no weight — it cannot discriminate between documents.
2. Hit rate @3 = 3 hits out of 4 queries = 0.75. MRR @3
   = (1/1 + 1/2 + 0 + 1/1) / 4 = (1 + 0.5 + 0 + 1) / 4
   = 2.5 / 4 = 0.625. The absent query contributes 0 to both.
3. (a) Small chunks win the detail question: 0.468 vs 0.155, a
   gap of 0.313. The focused chunk is not diluted by neighbors.
   (b) With one chunk allowed, the best small chunk covers 50%
   of the spanning question (it holds only one of the two fact
   sentences), while the best large chunk covers 100% (it holds
   both). Precision favors small; coverage favors large.
4. Layer 3, retrieved-content sanitization. The user-input phrase
   scan only inspects the user's own words; indirect attacks arrive
   inside documents the system fetched, so the scan never sees the
   hostile text at all.
5. Mechanism: the answer is built from passages fetched at answer
   time, so specifics come from sources rather than from the
   model's memory — fewer invented details. Limit: retrieval can
   still mislead — if it returns the wrong passages, the answer
   inherits their errors, and if a passage itself carries injected
   instructions, the model may follow them (indirect injection).
