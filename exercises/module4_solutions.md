# Module 4 solutions — Fine-tuning or RAG? The decision workflow

1. RAG. The facts change every quarter, and retrieval reads the
   current policy at answer time; fine-tuning would freeze last
   quarter's policy into the weights and need retraining every
   quarter to keep up.
2. Fine-tuning. The gap is behavior and format, not facts: no
   retrieved passage can teach the model to always emit that exact
   structure, but training on examples in that format can.
3. They skipped retrieval (ladder steps 2 and 4). Fine-tuning alone
   bakes prices in at training time. They should add RAG — or
   combine RAG with the fine-tuned model — so prices come from
   current sources while the trained behavior stays.
4. Retrieval is working (facts right) but behavior is wrong, so the
   failing rung is behavior, not knowledge. Step 3b, fine-tuning,
   fixes tone, format, and task skill — the things retrieval
   cannot supply.
5. The table leans toward RAG. Changing data favors retrieval
   because retrieved facts update the moment the documents update,
   while fine-tuned weights freeze facts at training time and go
   stale until the next training run.
