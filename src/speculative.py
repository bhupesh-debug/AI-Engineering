"""Speculative decoding, simulated.

Illustrative simulation only — no real model runs here. A normal
generating model writes one word at a time, each word waiting on the
last. Speculative decoding lets a small, fast draft model scribble
several candidate words ahead; the big model then checks the whole
batch at once and keeps the longest run it agrees with, plus one
corrected word of its own.

Plain-language idea: a fast junior assistant drafts a paragraph while
the senior editor reads it in one pass, crossing out from the first
mistake onward. The team still produces several approved words per
round instead of one — as long as the junior is usually right. When the
junior is usually wrong, the checking costs more than it saves, and the
simulation below shows that too.

Model of one step: the draft proposes k tokens. Each proposed token
matches what the big model would have written with probability alpha,
independently, and checking stops at the first mismatch. Tokens
produced per step = accepted prefix length + 1 (the verifier's own
correction word). Latency assumes one big-model step costs 1.0 unit and
one draft token costs t_draft units; verification of the batch costs
one big-model step because it runs in parallel.
"""

import random


def theoretical_tokens_per_step(alpha, draft_len):
    """Expected tokens per step: 1 + alpha + alpha**2 + ... + alpha**k."""
    return 1.0 + sum(alpha ** i for i in range(1, draft_len + 1))


def simulate(alpha, draft_len, steps, seed=7, t_draft=0.1, t_large=1.0):
    """Run the simulation; return (mean tokens/step, speedup vs 1-by-1).

    Speedup compares wall-clock time: baseline writes the same number
    of tokens one by one at t_large each, while speculation spends
    draft_len * t_draft + t_large per step.
    """
    rng = random.Random(seed)
    total_tokens = 0
    for _ in range(steps):
        accepted = 0
        for _ in range(draft_len):
            if rng.random() < alpha:
                accepted += 1
            else:
                break
        total_tokens += accepted + 1
    mean_tokens = total_tokens / steps
    time_per_step = draft_len * t_draft + t_large
    speedup = (mean_tokens * t_large) / time_per_step
    return mean_tokens, speedup


def ascii_bars(pairs, width=40):
    top = max(value for _, value in pairs) or 1.0
    lines = []
    for label, value in pairs:
        bar = "#" * max(1, int(round(value / top * width)))
        lines.append(f"{label:>12} | {bar} {value:.2f}")
    return "\n".join(lines)


def main():
    draft_len, steps = 4, 20000
    print("Speculative decoding simulation (draft proposes 4 tokens,")
    print("draft token cost 0.1, verifier step cost 1.0):")
    print()
    rows = []
    for alpha in [0.0, 0.3, 0.5, 0.7, 0.9, 1.0]:
        mean_tokens, speedup = simulate(alpha, draft_len, steps)
        theory = theoretical_tokens_per_step(alpha, draft_len)
        rows.append((alpha, mean_tokens, theory, speedup))
        print(f"  draft accuracy {alpha:.1f}: {mean_tokens:.2f} tokens/step "
              f"(theory {theory:.2f}), speedup {speedup:.2f}x")
    print()
    print("Mean tokens per step by draft accuracy:")
    print(ascii_bars([(f"alpha {a:.1f}", m) for a, m, _, _ in rows]))
    print()
    print("Reading: speculation only helps when the draft is decent.")
    print("At accuracy 0.0 the system is slower than one-by-one, because")
    print("it pays draft + verification cost for a single token.")


if __name__ == "__main__":
    main()
