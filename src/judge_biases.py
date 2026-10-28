"""Judge biases: a catalog of how an AI judge bends scores.

Deepens src/judge.py without changing it. The base demo catches one
bias (verbosity). This one demonstrates three, each with a concrete
toy example built from the same transparent rubric, plus the
mitigation that addresses that bias:

1. Verbosity bias — the same content, padded with filler, scores
   higher, because the rubric pays a length bonus. (Mechanism: any
   scoring rule that rewards length rewards padding.)
2. Position bias — when two answers tie on the rubric, a pairwise
   comparator that breaks ties by position picks whichever answer
   was shown first. Swap the order and the winner flips, although
   neither answer changed. (Mechanism: order leaks into the verdict.)
3. Self-enhancement bias — simulated here, stated as simulation: a
   judge that awards a bonus for its own house style (here, a
   recognizable marker phrase) inflates scores for answers written
   in that style, whatever their content. (Mechanism: the judge
   mistakes familiarity for quality.)

Plain-language idea: the star pupil grading homework has habits.
The pupil loves long essays (verbosity), likes whichever paper is
on top of the pile (position), and loves essays that sound like
their own writing (self-enhancement). None of these habits is
"cheating" — they are what happens when a grader's shortcuts go
unexamined. The fixes are boring on purpose: grade against a fixed
rubric, randomize order, hide authorship, and keep checking a sample
against human grades.

All scores below come from the base demo's rubric or from the
small, labeled simulation functions in this file — nothing here
measures a real model.
"""

try:
    from src.judge import FILLER, SAMPLES, judge_score
except ImportError:  # running as a script from inside src/
    from judge import FILLER, SAMPLES, judge_score

# The "full" sample is the strongest content in the base demo's set.
FULL_TEXT = next(s["text"] for s in SAMPLES if s["id"] == "full")
SHORT_TEXT = next(s["text"] for s in SAMPLES if s["id"] == "short")

# Marker phrase standing in for "the judge's own house style" in the
# self-enhancement simulation. No real model writes or prefers this
# phrase; it exists only to make the mechanism visible.
HOUSE_MARKER = "as a careful assistant, I note that"


def verbosity_demo():
    """Same content, with and without filler padding."""
    base = judge_score(FULL_TEXT)
    padded = judge_score(FULL_TEXT + " " + FILLER)
    return base, padded


def pairwise_pick(first, second):
    """Pairwise comparator: higher rubric score wins; ties go to the
    answer shown first. Returns the winning text."""
    if judge_score(first) >= judge_score(second):
        return first
    return second


def position_demo():
    """Two different but tied answers; swapping order flips the winner.

    Both texts cover exactly one rubric keyword, so both score 1.875.
    The comparator breaks ties by position, so the winner is decided
    by order alone — neither answer is better than the other.
    """
    answer_a = SHORT_TEXT  # "RAG uses retrieval." — covers "retrieval"
    answer_b = "RAG uses context."  # covers "context" — same score
    pick_ab = pairwise_pick(answer_a, answer_b)
    pick_ba = pairwise_pick(answer_b, answer_a)
    return pick_ab is answer_a, pick_ba is answer_b


def self_enhancement_demo():
    """Simulated judge with a house-style bonus, vs the plain rubric.

    The simulation adds +0.5 to any answer containing the house
    marker, capped at 5.0. Compare a plain answer with the same
    answer plus the marker: content identical, score inflated.
    """
    def styled_judge(text):
        score = judge_score(text)
        if HOUSE_MARKER.lower() in text.lower():
            score = min(5.0, score + 0.5)
        return score

    plain = judge_score(SHORT_TEXT)
    styled = styled_judge(HOUSE_MARKER + " " + SHORT_TEXT)
    return plain, styled


def main():
    print("Bias 1 — verbosity: same content, padded with filler.")
    base, padded = verbosity_demo()
    print(f"  base score:   {base:.2f}")
    print(f"  padded score: {padded:.2f}  (content unchanged, "
          f"score up {padded - base:.2f})")
    print("  mitigation: score against content only — drop the length")
    print("  bonus, or cap it, and check padded vs plain on a sample.")
    print()
    print("Bias 2 — position: two tied answers, order swapped.")
    first_wins_ab, first_wins_ba = position_demo()
    print(f"  shown A first, A wins: {first_wins_ab}")
    print(f"  shown B first, B wins: {first_wins_ba}")
    print("  mitigation: score each answer alone against the rubric,")
    print("  or run both orders and average — never trust one order.")
    print()
    print("Bias 3 — self-enhancement (SIMULATED judge with a")
    print("house-style bonus; mechanism demo, not a real model):")
    plain, styled = self_enhancement_demo()
    print(f"  plain answer:  {plain:.2f}")
    print(f"  same + marker: {styled:.2f}  (content unchanged, "
          f"score up {styled - plain:.2f})")
    print("  mitigation: hide authorship from the judge, use more")
    print("  than one judge, and keep calibrating against human grades.")


if __name__ == "__main__":
    main()
