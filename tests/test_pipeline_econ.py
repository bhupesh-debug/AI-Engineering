"""Tests for src/pipeline_econ.py."""

from src import pipeline_econ


def test_route_costs():
    assert pipeline_econ.route_cost("cache_hit") == (10, 0.02)
    assert pipeline_econ.route_cost("blocked") == (15, 0.03)
    assert pipeline_econ.route_cost("retrieved") == (900, 1.14)


def test_cache_hit_is_cheapest():
    ms_hit, _ = pipeline_econ.route_cost("cache_hit")
    ms_full, _ = pipeline_econ.route_cost("retrieved")
    assert ms_hit < ms_full / 50


def test_worked_traffic_comparison():
    mixed_ms, mixed_cost = pipeline_econ.traffic_cost(
        {"cache_hit": 40, "blocked": 5, "retrieved": 55})
    full_ms, full_cost = pipeline_econ.traffic_cost({"retrieved": 100})
    assert mixed_ms == 49975
    assert full_ms == 90000
    assert abs(mixed_cost - 63.65) < 1e-9
    assert abs(full_cost - 114.0) < 1e-9
    assert mixed_ms < full_ms
    assert mixed_cost < full_cost
