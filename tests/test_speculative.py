"""Tests for src/speculative.py."""

import pytest

from src import speculative


def test_perfect_draft_yields_full_batch_plus_correction():
    mean, _ = speculative.simulate(1.0, draft_len=4, steps=100, seed=1)
    assert mean == pytest.approx(5.0)


def test_useless_draft_yields_only_the_correction():
    mean, _ = speculative.simulate(0.0, draft_len=4, steps=100, seed=1)
    assert mean == pytest.approx(1.0)


def test_theoretical_tokens_per_step():
    assert speculative.theoretical_tokens_per_step(0.7, 4) == pytest.approx(
        1 + 0.7 + 0.49 + 0.343 + 0.2401)


def test_simulation_matches_theory():
    mean, _ = speculative.simulate(0.7, draft_len=4, steps=20000, seed=7)
    assert mean == pytest.approx(
        speculative.theoretical_tokens_per_step(0.7, 4), abs=0.05)


def test_better_draft_means_more_tokens():
    low, _ = speculative.simulate(0.3, draft_len=4, steps=20000, seed=7)
    high, _ = speculative.simulate(0.9, draft_len=4, steps=20000, seed=7)
    assert high > low


def test_speedup_only_when_draft_is_decent():
    _, fast = speculative.simulate(0.8, draft_len=4, steps=5000, seed=7)
    _, slow = speculative.simulate(0.0, draft_len=4, steps=5000, seed=7)
    assert fast > 1.0
    assert slow < 1.0
