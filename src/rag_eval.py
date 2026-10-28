"""RAG evaluation: retrieval quality and chunking, measured on toy data.

Deepens src/rag.py without changing it. All documents and queries are
synthetic and written for this project. Two questions are answered
with numbers, not opinions:

1. Retrieval quality: for queries whose correct document is known in
   advance, how often is it in the top k (hit rate), and how high does
   it rank (MRR — mean reciprocal rank)?
2. Chunking: does splitting one long note into small pieces help or
   hurt? Small chunks are precise for single-detail questions but can
   split an answer across a boundary; large chunks keep context
   together but dilute any single detail.

Plain-language idea: retrieval is a librarian fetching pages. Hit rate
asks "did the right book come back at all?" MRR asks "was it on top
of the pile or buried?" Chunking is how the librarian cuts the books:
thin pamphlets make one fact easy to find but tear a two-page
explanation in half; thick chapters keep explanations whole but make
one fact harder to spot.

Chunking here is simplified on purpose: "small" means one sentence per
chunk, "large" means four sentences per chunk. Real systems chunk by
tokens with overlap; the trade-off shape is the same.
"""

try:
    from src.rag import DOCUMENTS, retrieve
except ImportError:  # running as a script from inside src/
    from rag import DOCUMENTS, retrieve

# (query, id of the document that answers it) — ground truth by design.
QUERIES = [
    ("how do I stop prompt injection attacks", "defense"),
    ("what is LoRA fine tuning", "lora"),
    ("how does speculative decoding make inference faster", "speculative"),
    ("how does AI judge model outputs", "judge"),
    ("why cache repeated answers", "cache"),
    ("what is retrieval augmented generation", "rag"),
]

# One long synthetic note, built as sentences so chunk boundaries are
# exact. Sentence 3 holds a unique detail; sentences 4-5 hold a pair
# of facts that only make sense together.
LONG_SENTENCES = [
    "Retrieval augmented generation starts by searching a knowledge base "
    "for passages related to the question.",
    "The retrieved passages are pasted into the prompt so the model "
    "answers with fresh context instead of memory alone.",
    "The midnight ledger records every retrieval decision for later audit.",
    "The harbor atlas maps each source document to its owner team.",
    "Together the ledger and the atlas let reviewers trace any answer "
    "back to the passage and the person responsible for it.",
    "Good retrieval also ranks passages so the most relevant one is "
    "read first and weaker ones are ignored.",
    "When the knowledge base changes, the answers change with it, "
    "because nothing was baked into the model weights.",
    "That freshness is the main reason teams choose retrieval over "
    "retraining when facts move fast.",
]


def chunk_small(sentences=LONG_SENTENCES):
    """One sentence per chunk."""
    return list(sentences)


def chunk_large(sentences=LONG_SENTENCES, group=4):
    """Groups of `group` sentences per chunk."""
    return [" ".join(sentences[i:i + group])
            for i in range(0, len(sentences), group)]


def _docs_from_chunks(chunks):
    return [{"id": f"chunk-{i}", "title": f"chunk {i}", "text": text}
            for i, text in enumerate(chunks)]


def evaluate(queries=QUERIES, documents=DOCUMENTS, top_k=3):
    """Return (hit_rate, mrr, per-query ranks) for the given queries."""
    ranks = []
    for query, relevant_id in queries:
        ranked = retrieve(query, documents=documents, top_k=top_k)
        rank = None
        for i, (doc, _) in enumerate(ranked, start=1):
            if doc["id"] == relevant_id:
                rank = i
                break
        ranks.append(rank)
    hits = sum(1 for r in ranks if r is not None)
    hit_rate = hits / len(queries) if queries else 0.0
    mrr = (sum(1.0 / r for r in ranks if r is not None) / len(queries)
           if queries else 0.0)
    return hit_rate, mrr, ranks


def chunking_comparison():
    """Best-chunk cosine and term coverage for detail vs spanning queries.

    Detail query: both rare words live in one sentence, so the small
    chunk holding it is focused and scores high, while the large chunk
    is diluted by its neighbors. Spanning query: rare words live in
    two adjacent sentences that share a large chunk but sit in
    different small chunks. Cosine alone favors the small chunk even
    here (dilution beats coverage in the dot product), so coverage is
    reported too: with one chunk allowed, the small chunk covers only
    half the spanning question, the large chunk covers all of it.
    In practice, retrieving top-k small chunks recovers the split
    context — the lesson is about single-chunk coverage, not a
    verdict that one size always wins.
    """
    small_docs = _docs_from_chunks(chunk_small())
    large_docs = _docs_from_chunks(chunk_large())
    results = {}
    for name, query in [("detail", "midnight ledger"),
                        ("spanning", "midnight ledger harbor atlas")]:
        small = retrieve(query, documents=small_docs, top_k=1)
        large = retrieve(query, documents=large_docs, top_k=1)
        small_text = small[0][0]["text"] if small else ""
        large_text = large[0][0]["text"] if large else ""
        query_terms = set(query.split())
        small_cov = (len([t for t in query_terms if t in small_text])
                     / len(query_terms)) if query_terms else 0.0
        large_cov = (len([t for t in query_terms if t in large_text])
                     / len(query_terms)) if query_terms else 0.0
        results[name] = {
            "small_best": small[0][1] if small else 0.0,
            "large_best": large[0][1] if large else 0.0,
            "small_coverage": small_cov,
            "large_coverage": large_cov,
        }
    return results


def main():
    print("Retrieval quality on 6 queries with known answers (top 3):")
    hit_rate, mrr, ranks = evaluate()
    for (query, relevant_id), rank in zip(QUERIES, ranks):
        print(f"  rank {rank if rank else '-'}: {query!r} -> {relevant_id}")
    print(f"  hit rate @3: {hit_rate:.2f}")
    print(f"  MRR @3:      {mrr:.3f}")
    print()
    print("Chunking comparison (best-chunk cosine, then query-term")
    print("coverage of that chunk — one chunk allowed):")
    comp = chunking_comparison()
    for name, row in comp.items():
        print(f"  {name:>9} query: small cosine={row['small_best']:.3f} "
              f"(covers {row['small_coverage']:.0%} of the question), "
              f"large cosine={row['large_best']:.3f} "
              f"(covers {row['large_coverage']:.0%})")
    print()
    print("Reading: small chunks win on precision (detail question),")
    print("large chunks win on coverage (spanning question, one chunk")
    print("allowed). Retrieving top-k small chunks recovers split")
    print("context in practice — neither size wins everywhere.")


if __name__ == "__main__":
    main()
