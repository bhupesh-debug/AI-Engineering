"""Tests for src/lora.py."""

import pytest

from src import lora


def test_parameter_counts():
    assert lora.parameter_counts(10, 8, 2) == (80, 36)
    full, small = lora.parameter_counts(512, 512, 4)
    assert full == 262144
    assert small == 4096
    assert small < full


def test_rank_of_known_matrices():
    assert lora.rank_small([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    assert lora.rank_small([[0, 0], [0, 0]]) == 0
    assert lora.rank_small([[2, 4], [1, 2]]) == 1


def test_matmul_paths_agree():
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[7, 8], [9, 10], [11, 12]]
    expected = [[58, 64], [139, 154]]
    assert lora.matmul_pure(a, b) == expected
    got = lora.to_lists(lora.matmul(a, b))
    assert all(got[i][j] == pytest.approx(expected[i][j])
               for i in range(2) for j in range(2))


def test_adapter_training_improves_and_keeps_base_frozen():
    before, after, base_before, base_after, update = lora.train_adapter()
    assert after < before
    assert after < 0.05
    assert base_before == base_after
    assert lora.rank_small(update) == 1
