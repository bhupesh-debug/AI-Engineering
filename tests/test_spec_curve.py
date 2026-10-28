"""Tests for src/spec_curve.py."""

from src import spec_curve


def test_breakeven_values():
    assert abs(spec_curve.breakeven(4) - 0.287) < 0.01
    assert abs(spec_curve.breakeven(8) - 0.445) < 0.01
    assert spec_curve.breakeven(8) > spec_curve.breakeven(4)


def test_speedup_crosses_one():
    rows = {row["alpha"]: row for row in spec_curve.curve(4, steps=20000)}
    assert rows[0.0]["speedup"] < 1.0
    assert rows[0.9]["speedup"] > 1.0


def test_simulation_matches_theory():
    for row in spec_curve.curve(4, steps=20000):
        assert abs(row["simulated"] - row["theory"]) < 0.1


def test_speedup_monotone_in_accuracy():
    speedups = [row["speedup"] for row in spec_curve.curve(4, steps=20000)]
    assert all(a < b for a, b in zip(speedups, speedups[1:]))
