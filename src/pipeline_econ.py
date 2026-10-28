"""Pipeline economics: what each route through the system costs.

Deepens src/pipeline.py without changing it. The base demo shows the
route a request takes; this one prices each route. Unit prices below
are toy numbers chosen to make the arithmetic visible — they are NOT
vendor prices, measurements, or benchmarks. What is real is the
shape: cache hits skip the expensive stages, blocked requests stop
early, and only full retrieval-plus-generation pays for everything.

Stage costs (toy units; time in milliseconds, money in abstract
cost units — the point is the comparison, not the currency):
- cache check:    5 ms,  0.01
- guardrail check: 10 ms, 0.02
- retrieval:      80 ms,  0.10
- generation:    800 ms,  1.00
- feedback log:   5 ms,  0.01

Routes mirror src/pipeline.py exactly: a cache hit serves from the
cache then logs feedback; a blocked request stops after the
guardrail and logs nothing (the base demo returns early there);
a full request pays for every stage.

Plain-language idea: a library that answers from the pinned board
(cache) spends almost nothing; a question that must be researched
and written fresh pays for the librarian's whole afternoon. The
worked comparison below shows what a day of mixed traffic costs
versus a day where every question is researched fresh — and why a
high cache-hit rate is worth more than a slightly cheaper model.
"""

# (milliseconds, cost units) per stage — toy numbers, labeled as such.
STAGE_COSTS = {
    "cache": (5, 0.01),
    "guardrail": (10, 0.02),
    "retrieval": (80, 0.10),
    "generation": (800, 1.00),
    "feedback": (5, 0.01),
}

# Stages each route actually walks, mirroring src/pipeline.py.
ROUTES = {
    "cache_hit": ["cache", "feedback"],
    "blocked": ["cache", "guardrail"],
    "retrieved": ["cache", "guardrail", "retrieval", "generation",
                  "feedback"],
}


def route_cost(route):
    """(total ms, total cost units) for one request on this route."""
    stages = ROUTES[route]
    ms = sum(STAGE_COSTS[s][0] for s in stages)
    cost = sum(STAGE_COSTS[s][1] for s in stages)
    return ms, cost


def traffic_cost(mix):
    """Total (ms, cost) for a traffic mix: {route: request_count}."""
    total_ms = sum(route_cost(r)[0] * n for r, n in mix.items())
    total_cost = sum(route_cost(r)[1] * n for r, n in mix.items())
    return total_ms, total_cost


def main():
    print("Per-request cost by route (toy units):")
    for route in ["cache_hit", "blocked", "retrieved"]:
        ms, cost = route_cost(route)
        print(f"  {route:>10}: {ms:>4} ms, {cost:.2f} cost units "
              f"({', '.join(ROUTES[route])})")
    print()
    # Worked comparison: 100 requests, mixed vs all-full-path.
    mix = {"cache_hit": 40, "blocked": 5, "retrieved": 55}
    mixed_ms, mixed_cost = traffic_cost(mix)
    full_ms, full_cost = traffic_cost({"retrieved": 100})
    print("Worked comparison, 100 requests:")
    print(f"  mixed traffic (40 cached, 5 blocked, 55 full): "
          f"{mixed_ms:,} ms, {mixed_cost:.2f} units")
    print(f"  all 100 through the full path: "
          f"{full_ms:,} ms, {full_cost:.2f} units")
    print(f"  saved by cache + early blocking: "
          f"{full_ms - mixed_ms:,} ms "
          f"({100.0 * (1 - mixed_ms / full_ms):.1f}% faster), "
          f"{full_cost - mixed_cost:.2f} units "
          f"({100.0 * (1 - mixed_cost / full_cost):.1f}% cheaper)")
    print()
    print("Reading: the cache is the cheapest performance win in the")
    print("whole architecture — one cache hit costs about 1% of a")
    print("full request. Guardrails cost almost nothing and stop")
    print("bad requests before the expensive stages run.")


if __name__ == "__main__":
    main()
