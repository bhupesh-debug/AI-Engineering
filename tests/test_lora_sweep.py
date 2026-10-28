"""Tests for src/lora_sweep.py."""

from src import lora_sweep


def test_sweep_table_parameter_counts():
    rows = {row["rank"]: row for row in lora_sweep.sweep_table()}
    assert rows[4]["full"] == 262144
    assert rows[4]["lora"] == 4096
    assert rows[1]["lora"] == 1024
    assert rows[16]["lora"] == 16384


def test_captured_energy_monotone_and_bounded():
    values = [lora_sweep.captured_energy(r)
              for r in lora_sweep.RANKS]
    assert all(a < b for a, b in zip(values, values[1:]))
    assert abs(values[0] - 0.36) < 1e-6
    assert values[-1] > 0.99
    assert values[-1] < 1.0


def test_trained_loss_falls_with_rank():
    _, loss1 = lora_sweep.train_rank(1)
    _, loss2 = lora_sweep.train_rank(2)
    _, loss3 = lora_sweep.train_rank(3)
    assert loss1 > loss2 > loss3
    assert loss3 < 0.01


def test_spectrum_has_more_directions_than_max_rank():
    assert len(lora_sweep.SPECTRUM) > max(lora_sweep.RANKS)
