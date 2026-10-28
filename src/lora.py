"""LoRA (Low-Rank Adaptation): parameter math plus a tiny trained adapter.

Illustrative demo only. All dimensions below are toy sizes chosen to
make the arithmetic visible — they are not the dimensions of any real
model. LoRA freezes a model's original weights and trains only two
small matrices whose product is the update. Because the update is built
as a product of a tall-thin matrix and a short-wide one, its rank can
never exceed the small inner size — that is the whole trick.

Plain-language idea: imagine a giant frozen statue (the base model).
You are not allowed to re-carve it. Instead you may attach small clay
patches (the adapter). A patch that only needs a few directions of
change can be described by two thin strips of numbers instead of one
huge slab — and you can keep a different patch for every job while the
one statue stays shared.

This demo uses numpy for matrix multiplication when it is available
and falls back to pure Python otherwise, so it runs either way. The
toy training itself is pure Python, so its numbers are identical in
both cases.
"""

try:
    import numpy as _np
except ImportError:  # pragma: no cover - exercised via the fallback path
    _np = None


def matmul_pure(a, b):
    """Plain-Python matrix product (lists of lists)."""
    rows, inner, cols = len(a), len(b), len(b[0])
    out = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            if a[i][k] != 0.0:
                for j in range(cols):
                    out[i][j] += a[i][k] * b[k][j]
    return out


def matmul(a, b):
    """Matrix product: numpy when available, pure Python otherwise."""
    if _np is not None:
        return _np.asarray(a, dtype=float) @ _np.asarray(b, dtype=float)
    return matmul_pure(a, b)


def to_lists(matrix):
    """Normalize a numpy array or list-of-lists to lists of floats."""
    if _np is not None and isinstance(matrix, _np.ndarray):
        return matrix.tolist()
    return [[float(v) for v in row] for row in matrix]


def parameter_counts(in_dim, out_dim, rank):
    """Full fine-tune vs LoRA trainable parameter counts."""
    full = in_dim * out_dim
    lora = rank * (in_dim + out_dim)
    return full, lora


def rank_small(matrix, tol=1e-9):
    """Rank of a small matrix by Gaussian elimination (teaching code)."""
    rows = [list(map(float, row)) for row in matrix]
    if not rows:
        return 0
    n_rows, n_cols = len(rows), len(rows[0])
    rank, r = 0, 0
    for c in range(n_cols):
        pivot = None
        for i in range(r, n_rows):
            if abs(rows[i][c]) > tol:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = rows[r][c]
        rows[r] = [v / scale for v in rows[r]]
        for i in range(n_rows):
            if i != r and abs(rows[i][c]) > tol:
                factor = rows[i][c]
                rows[i] = [v - factor * w for v, w in zip(rows[i], rows[r])]
        r += 1
        rank += 1
        if r == n_rows:
            break
    return rank


def train_adapter(steps=300, lr=0.5):
    """Train a rank-1 adapter on a toy task; base weights stay frozen.

    The base matrix reads only the first two inputs, so it cannot solve
    a task that also depends on the third input. The adapter (one
    column times one row) learns exactly that missing direction.
    Returns (loss_before, loss_after, base_before, base_after, update).
    """
    base = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]  # 2 outputs x 3 inputs
    # (input, target) pairs; the third input matters, so base alone fails.
    data = [
        ([1.0, 0.0, 0.0], [1.0, 0.0]),
        ([0.0, 1.0, 0.0], [0.0, 1.0]),
        ([0.0, 0.0, 1.0], [1.0, 1.0]),
        ([1.0, 1.0, 1.0], [2.0, 2.0]),
    ]
    adapter_b = [0.1, 0.1]       # 2 x 1
    adapter_a = [0.1, 0.1, 0.1]  # 1 x 3

    def loss_and_grads():
        n, d = len(data), 2
        total, grad_b = 0.0, [0.0, 0.0]
        grad_a = [0.0, 0.0, 0.0]
        for x, y in data:
            s = sum(adapter_a[i] * x[i] for i in range(3))
            base_out = [sum(base[j][i] * x[i] for i in range(3))
                        for j in range(2)]
            pred = [base_out[j] + adapter_b[j] * s for j in range(2)]
            err = [pred[j] - y[j] for j in range(2)]
            total += sum(e * e for e in err)
            # d loss / d pred = 2 * err / (n * d)
            d_pred = [2.0 * e / (n * d) for e in err]
            for j in range(2):
                grad_b[j] += d_pred[j] * s
            d_s = sum(d_pred[j] * adapter_b[j] for j in range(2))
            for i in range(3):
                grad_a[i] += d_s * x[i]
        return total / (n * d), grad_b, grad_a

    loss_before, _, _ = loss_and_grads()
    base_before = [row[:] for row in base]
    for _ in range(steps):
        _, grad_b, grad_a = loss_and_grads()
        adapter_b = [b - lr * g for b, g in zip(adapter_b, grad_b)]
        adapter_a = [a - lr * g for a, g in zip(adapter_a, grad_a)]
    loss_after, _, _ = loss_and_grads()
    update = [[adapter_b[j] * adapter_a[i] for i in range(3)]
              for j in range(2)]
    return loss_before, loss_after, base_before, base, update


def main():
    print("Parameter math for a toy layer (illustrative sizes only,")
    print("not a real model's dimensions):")
    print(f"{'rank':>6} {'full':>12} {'LoRA':>12} {'saved':>8}")
    for rank in [1, 2, 4, 8, 16]:
        full, lora = parameter_counts(512, 512, rank)
        print(f"{rank:>6} {full:>12,} {lora:>12,} "
              f"{100.0 * (1 - lora / full):>7.1f}%")
    print()
    print("Full fine-tuning trains every weight; LoRA trains only the")
    print("two thin adapter matrices — and one base model can host a")
    print("different adapter per task.")
    print()
    loss_before, loss_after, base_before, base_after, update = \
        train_adapter()
    print("Toy training: frozen 2x3 base + rank-1 adapter")
    print(f"  loss before adapter training: {loss_before:.4f}")
    print(f"  loss after adapter training:  {loss_after:.4f}")
    print(f"  base weights unchanged: {base_before == base_after}")
    print(f"  adapter update shape: 2x3, rank: {rank_small(update)} "
          "(built as a 2x1 times 1x3 product, so rank <= 1 by design)")
    print()
    print("  base W (frozen)      +  adapter update (trained)")
    print("  [1 0 0]                   [b1*a1 b1*a2 b1*a3]")
    print("  [0 1 0]                   [b2*a1 b2*a2 b2*a3]")


if __name__ == "__main__":
    main()
