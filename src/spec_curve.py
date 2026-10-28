"""Speculative decoding curve: exactly where it stops helping.

Deepens src/speculative.py without changing it. The base demo shows
one draft accuracy; this one sweeps draft accuracy from 0.0 to 0.95
at two draft lengths and finds the breakeven point — the accuracy
below which speculation is slower than generating one token at a
time. The breakeven is computed from the simulation's own cost
model (one big-model step costs 1.0, each draft token costs 0.1),
not asserted: speedup crosses 1.0 where expected tokens per step
exceed the per-step cost.

Plain-language idea: the junior assistant drafts, the senior editor
checks. If the junior is right most of the time, each checking round
approves several words and the team flies. If the junior is usually
wrong, the editor throws nearly every draft away and still pays the
checking round — the team moves slower than the editor working
alone. The curve below finds the junior's minimum useful accuracy.
"""

try:
    from src.speculative import theoretical_tokens_per_step, simulate
except ImportError:  # running as a script from inside src/
    from speculative import theoretical_tokens_per_step, simulate

ALPHAS = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95]
STEPS = 20000


def curve(draft_len, alphas=ALPHAS, steps=STEPS, t_draft=0.1,
          t_large=1.0):
    """One row per draft accuracy: theory tokens/step, simulated
    tokens/step, and simulated speedup. Simulation uses the same
    fixed seed as the base demo, so it is reproducible."""
    rows = []
    for alpha in alphas:
        theory = theoretical_tokens_per_step(alpha, draft_len)
        mean_tokens, speedup = simulate(alpha, draft_len, steps,
                                        t_draft=t_draft, t_large=t_large)
        rows.append({"alpha": alpha, "theory": theory,
                     "simulated": mean_tokens, "speedup": speedup})
    return rows


def breakeven(draft_len, t_draft=0.1, t_large=1.0, lo=0.0, hi=1.0,
              tol=0.001):
    """Draft accuracy where speedup crosses 1.0, by bisection on the
    exact theory curve. Returns None if it never crosses in [0, 1]."""
    cost = draft_len * t_draft + t_large

    def speedup(alpha):
        return theoretical_tokens_per_step(alpha, draft_len) / cost

    if speedup(hi) <= 1.0:
        return None
    while hi - lo > tol:
        mid = (lo + hi) / 2.0
        if speedup(mid) < 1.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main():
    for draft_len in [4, 8]:
        print(f"Draft length {draft_len} "
              f"(per-step cost {draft_len * 0.1 + 1.0:.1f} units):")
        print(f"{'alpha':>6} {'theory tok/step':>16} "
              f"{'sim tok/step':>13} {'speedup':>8}")
        for row in curve(draft_len):
            print(f"{row['alpha']:>6.2f} {row['theory']:>16.3f} "
                  f"{row['simulated']:>13.3f} {row['speedup']:>8.3f}")
        point = breakeven(draft_len)
        print(f"  breakeven draft accuracy: "
              f"{point:.3f}" if point is not None else "  never helps")
        print()
    print("Reading: longer drafts raise the ceiling (more tokens per")
    print("round when the drafter is good) AND the floor (more wasted")
    print("drafting when it is bad). Below breakeven, speculation")
    print("costs more than it saves — turn it off, don't tune it.")


if __name__ == "__main__":
    main()
