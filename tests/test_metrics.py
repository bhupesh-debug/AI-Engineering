"""Tests for src/metrics.py."""

import pytest

from src import metrics


def test_entropy_of_fair_coin_is_one_bit():
    assert metrics.entropy_of_distribution([0.5, 0.5]) == pytest.approx(1.0)


def test_entropy_of_certainty_is_zero():
    assert metrics.entropy_of_distribution([1.0]) == pytest.approx(0.0)


def test_entropy_of_known_distribution():
    assert metrics.entropy_of_distribution([0.5, 0.25, 0.25]) == pytest.approx(1.5)


def test_perplexity_is_two_to_the_entropy():
    assert metrics.perplexity_from_entropy(1.0) == pytest.approx(2.0)
    assert metrics.perplexity_from_entropy(0.0) == pytest.approx(1.0)


def test_unigram_distribution_sums_to_one():
    probs, total = metrics.unigram_distribution(metrics.TOY_CORPUS)
    assert sum(probs.values()) == pytest.approx(1.0)
    assert total == 23


def test_typical_sentence_beats_surprising_sentence():
    probs, total = metrics.unigram_distribution(metrics.TOY_CORPUS)
    typical = metrics.sentence_perplexity("the cat sat on the mat", probs, total)
    odd = metrics.sentence_perplexity("quantum banana orbits zebra", probs, total)
    assert typical > 0
    assert odd > typical
