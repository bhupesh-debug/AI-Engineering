"""Tests for src/rag_eval.py."""

from src import rag_eval


def test_evaluate_perfect_on_known_queries():
    hit_rate, mrr, ranks = rag_eval.evaluate()
    assert hit_rate == 1.0
    assert mrr == 1.0
    assert ranks == [1, 1, 1, 1, 1, 1]


def test_evaluate_miss_counts_as_zero():
    # A query sharing no words with any document scores 0 everywhere,
    # so the top 3 are just the first three documents; "cache" (the
    # sixth document) is genuinely absent from the ranking.
    hit_rate, mrr, ranks = rag_eval.evaluate(
        queries=[("nonsense query about nothing", "cache")], top_k=3)
    assert ranks == [None]
    assert hit_rate == 0.0
    assert mrr == 0.0


def test_chunk_counts():
    assert len(rag_eval.chunk_small()) == 8
    assert len(rag_eval.chunk_large()) == 2


def test_detail_query_small_chunk_more_precise():
    comp = rag_eval.chunking_comparison()
    assert comp["detail"]["small_best"] > comp["detail"]["large_best"]
    assert comp["detail"]["small_coverage"] == 1.0
    assert comp["detail"]["large_coverage"] == 1.0


def test_spanning_query_large_chunk_covers_more():
    comp = rag_eval.chunking_comparison()
    assert comp["spanning"]["small_coverage"] == 0.5
    assert comp["spanning"]["large_coverage"] == 1.0
