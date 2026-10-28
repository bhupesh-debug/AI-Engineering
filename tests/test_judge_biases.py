"""Tests for src/judge_biases.py."""

from src import judge_biases


def test_verbosity_bias_is_half_a_point():
    base, padded = judge_biases.verbosity_demo()
    assert padded - base == 0.5


def test_position_bias_flips_with_order():
    first_wins_ab, first_wins_ba = judge_biases.position_demo()
    assert first_wins_ab is True
    assert first_wins_ba is True


def test_self_enhancement_bias_is_half_a_point():
    plain, styled = judge_biases.self_enhancement_demo()
    assert styled - plain == 0.5


def test_pairwise_pick_prefers_higher_score():
    strong = "RAG uses retrieval to fetch knowledge context and reduce hallucination."
    weak = "RAG uses retrieval."
    assert judge_biases.pairwise_pick(strong, weak) is strong
    assert judge_biases.pairwise_pick(weak, strong) is strong
