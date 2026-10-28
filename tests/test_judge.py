"""Tests for src/judge.py."""

import pytest

from src import judge


def test_judge_scores_stay_on_scale():
    for sample in judge.SAMPLES:
        assert 1.0 <= judge.judge_score(sample["text"]) <= 5.0


def test_judge_scores_for_known_texts():
    assert judge.judge_score(judge.SAMPLES[0]["text"]) == pytest.approx(4.5)
    assert judge.judge_score(judge.SAMPLES[1]["text"]) == pytest.approx(1.875)
    assert judge.judge_score(judge.SAMPLES[3]["text"]) == pytest.approx(1.0)


def test_agreement_is_strong_but_not_perfect():
    pairs = [(judge.judge_score(s["text"]), s["human"]) for s in judge.SAMPLES]
    assert judge.mean_absolute_error(pairs) < 0.5
    judges = [j for j, _ in pairs]
    humans = [h for _, h in pairs]
    assert judge.pearson(judges, humans) > 0.9


def test_verbosity_bias_padded_beats_concise():
    concise = judge.SAMPLES[0]["text"]
    padded = concise + " " + judge.FILLER
    assert len(padded.split()) > 60
    assert judge.judge_score(padded) > judge.judge_score(concise)


def test_metric_helpers():
    assert judge.mean_absolute_error([(5, 5), (3, 4)]) == pytest.approx(0.5)
    assert judge.pearson([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)
