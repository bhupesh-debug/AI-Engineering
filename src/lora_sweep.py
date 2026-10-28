"""LoRA rank sweep: what bigger adapters buy you, and what they cost.

Deepens src/lora.py without changing it. Two views of the same
trade-off, both on toy numbers:

1. Parameter counts for a 512x512 toy layer across ranks 1/2/4/8/16,
   from the same formula as the base demo.
2. Approximation quality: suppose the change a task truly needs has
   directions of shrinking importance (a synthetic spectrum decaying
   by half each step). A rank-r adapter can capture only the first r
   directions, so captured energy rises and residual error falls as
   rank grows — with diminishing returns. This is the best case a
   rank-r adapter can do (exact math, not training luck), which is
   why it is labeled a bound, not a result.
3. A trained check on a tiny task whose needed change genuinely has
   three directions: rank-1 and rank-2 adapters leave real error
   behind, rank-3 closes it. The base demo's task needed only one
   direction, which is why rank 1 already solved it there — rank
   helps exactly as much as the task's true complexity demands.

Plain-language idea: rank is how many independent directions your
clay patch can bend. A patch that bends one way fixes a one-way
problem perfectly and is useless for a three-way problem. Bigger
patches cost more clay (parameters) and capture more directions,
but each extra direction matters less than the last.
"""

try:
    from src.lora import parameter_counts, rank_small
except ImportError:  # running as a script from inside src/
    from lora import parameter_counts, rank_small

RANKS = [1, 2, 4, 8, 16]
LAYER_DIM = 512

# Synthetic spectrum: 32 directions, importance decaying by 0.8 each
# step. Energy of a direction is its squared size; totals are exact.
SPECTRUM = [64.0 * (0.8 ** i) for i in range(32)]


def captured_energy(rank, spectrum=SPECTRUM):
    """Fraction of total energy the first `rank` directions hold."""
    total = sum(s * s for s in spectrum)
    kept = sum(s * s for s in spectrum[:rank])
    return kept / total if total else 0.0


def sweep_table(ranks=RANKS, in_dim=LAYER_DIM, out_dim=LAYER_DIM):
    """One row per rank: params, saving, captured energy, residual."""
    rows = []
    for rank in ranks:
        full, lora = parameter_counts(in_dim, out_dim, rank)
        captured = captured_energy(rank)
        rows.append({
            "rank": rank,
            "full": full,
            "lora": lora,
            "saved_pct": 100.0 * (1 - lora / full),
            "captured_pct": 100.0 * captured,
            "residual_pct": 100.0 * (1 - captured),
        })
    return rows


# --- Trained check: a task whose needed change has three directions ---
# Base reads inputs 1-3 straight through; the task also needs input 4
# routed to output 1, input 3 added to output 2, and input 2 added to
# output 3. Those three extra directions are independent (rank 3).
BASE = [[1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0]]
DELTA = [[0.0, 0.0, 0.0, 1.0],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 1.0, 0.0, 0.0]]
DATA = [
    ([1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0]),
    ([0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 1.0]),
    ([0.0, 0.0, 1.0, 0.0], [0.0, 1.0, 1.0]),
    ([0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0]),
    ([1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0]),
    ([1.0, 0.0, 1.0, 0.0], [1.0, 1.0, 1.0]),
    ([0.0, 1.0, 0.0, 1.0], [1.0, 1.0, 1.0]),
    ([1.0, 1.0, 0.0, 1.0], [2.0, 1.0, 1.0]),
]


def train_rank(rank, steps=3000, lr=0.5):
    """Train a rank-`rank` adapter on the 3-direction task.

    Returns (loss_before, loss_after). Base stays frozen; only the
    two thin adapter matrices move. Fixed small init, no randomness,
    so results are reproducible.
    """
    n_out, n_in = 3, 4
    # Varied fixed init per component (NOT all-equal: identical starts
    # keep every rank component in lockstep forever, which silently
    # caps every rank at rank-1 behavior — the classic symmetry trap).
    b_mat = [[0.1 + 0.02 * ((j * 2 + k) % 5) for k in range(rank)]
             for j in range(n_out)]
    a_mat = [[0.1 + 0.02 * ((k * 3 + i) % 5) for i in range(n_in)]
             for k in range(rank)]

    def loss_and_grads():
        n, d = len(DATA), n_out
        total = 0.0
        grad_b = [[0.0] * rank for _ in range(n_out)]
        grad_a = [[0.0] * n_in for _ in range(rank)]
        for x, y in DATA:
            s = [sum(a_mat[k][i] * x[i] for i in range(n_in))
                 for k in range(rank)]
            base_out = [sum(BASE[j][i] * x[i] for i in range(n_in))
                        for j in range(n_out)]
            pred = [base_out[j] + sum(b_mat[j][k] * s[k]
                                      for k in range(rank))
                    for j in range(n_out)]
            err = [pred[j] - y[j] for j in range(n_out)]
            total += sum(e * e for e in err)
            d_pred = [2.0 * e / (n * d) for e in err]
            for j in range(n_out):
                for k in range(rank):
                    grad_b[j][k] += d_pred[j] * s[k]
            d_s = [sum(d_pred[j] * b_mat[j][k] for j in range(n_out))
                   for k in range(rank)]
            for k in range(rank):
                for i in range(n_in):
                    grad_a[k][i] += d_s[k] * x[i]
        return total / (n * d), grad_b, grad_a

    loss_before, _, _ = loss_and_grads()
    for _ in range(steps):
        _, grad_b, grad_a = loss_and_grads()
        b_mat = [[b - lr * g for b, g in zip(row_b, row_g)]
                 for row_b, row_g in zip(b_mat, grad_b)]
        a_mat = [[a - lr * g for a, g in zip(row_a, row_g)]
                 for row_a, row_g in zip(a_mat, grad_a)]
    loss_after, _, _ = loss_and_grads()
    return loss_before, loss_after


def main():
    print("Rank sweep for a 512x512 toy layer (analytic bound + cost):")
    print(f"{'rank':>5} {'LoRA params':>12} {'saved':>8} "
          f"{'captured':>9} {'residual':>9}")
    for row in sweep_table():
        print(f"{row['rank']:>5} {row['lora']:>12,} "
              f"{row['saved_pct']:>7.1f}% {row['captured_pct']:>8.2f}% "
              f"{row['residual_pct']:>8.2f}%")
    print()
    print("Trained check on a task needing 3 directions (loss, lower")
    print("is better; rank 1 already solved the base demo's 1-direction")
    print("task, so this task is deliberately harder):")
    for rank in [1, 2, 3]:
        before, after = train_rank(rank)
        print(f"  rank {rank}: loss {before:.4f} -> {after:.4f}")
    print()
    print("Reading: cost grows linearly with rank, captured value")
    print("grows with diminishing returns, and no rank helps past")
    print("the task's true number of directions.")


if __name__ == "__main__":
    main()
