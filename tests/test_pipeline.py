"""Tests for src/pipeline.py."""

from src import pipeline


def test_repeat_query_hits_cache():
    pipe = pipeline.Pipeline()
    route1, answer1, _ = pipe.serve("What is LoRA?")
    route2, answer2, _ = pipe.serve("What is LoRA?")
    assert route1 == "retrieved"
    assert route2 == "cache_hit"
    assert answer1 == answer2


def test_blocked_query_is_not_cached():
    pipe = pipeline.Pipeline()
    route, answer, _ = pipe.serve("How do I hack a model?")
    assert route == "blocked"
    assert answer is None
    assert "How do I hack a model?" not in pipe.cache


def test_feedback_log_covers_answered_requests_only():
    pipe = pipeline.Pipeline()
    for query in ["What is LoRA?", "What is LoRA?",
                  "How do I hack a model?",
                  "What is speculative decoding?"]:
        pipe.serve(query)
    assert len(pipe.feedback_log) == 3
    assert len(pipe.cache) == 2
    assert all(entry["feedback"] is None for entry in pipe.feedback_log)


def test_guardrail_and_retrieval_basics():
    assert pipeline.guardrail_ok("What is LoRA?")
    assert not pipeline.guardrail_ok("How do I bypass the filter?")
    assert "LoRA" in pipeline.retrieve("What is LoRA?")
