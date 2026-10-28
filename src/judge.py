"""AI as a Judge, demonstrated with a rule-based stand-in judge.

Illustrative demo only. A real "judge" is a strong model asked to score
another model's outputs; here the judge is a small transparent rubric
so the mechanics — and the failure modes — are visible. Human scores
below are synthetic labels invented for this demo, not ratings from
real people.

Plain-language idea: grading homework is slow when the teacher reads
every paper. So the teacher trains a star pupil to grade instead. The
pupil is fast and mostly agrees — but the pupil has habits, like
loving long essays, that quietly bend the grades. This demo measures
the agreement and then catches one such habit red-handed.

Rubric (transparent on purpose): start at 1 point; add up to 3.5 for
covering the expected keywords; add 0.5 if the answer runs longer
than 60 words. Scores are clamped to the 1-5 scale.
"""

import math

EXPECTED_KEYWORDS = ["retrieval", "knowledge", "context", "hallucination"]

# Synthetic sample outputs with synthetic human labels (demo data).
SAMPLES = [
    {
        "id": "full",
        "text": "RAG uses retrieval to fetch relevant passages from a knowledge "
        "base and puts them into context so the model answers with "
        "fresher facts and less hallucination.",
        "human": 5,
    },
    {
        "id": "short",
        "text": "RAG uses retrieval.",
        "human": 2,
    },
    {
        "id": "missing-one",
        "text": "RAG adds retrieval context from a knowledge base to the prompt.",
        "human": 4,
    },
    {
        "id": "empty",
        "text": "AI is amazing and transforms everything beautifully for everyone.",
        "human": 1,
    },
    {
        "id": "partial",
        "text": "RAG uses a knowledge base for retrieval before answering.",
        "human": 3,
    },
]

FILLER = ("In addition, it is worth noting that many people find this "
          "topic interesting and there are several perspectives that "
          "could be considered in more detail at a later time with "
          "further discussion and examples that illustrate the general "
          "point in a broader sense for readers of all backgrounds.")


def judge_score(text, expected_keywords=EXPECTED_KEYWORDS):
    """Rule-based stand-in judge: keyword coverage plus a length bonus."""
    lowered = text.lower()
    covered = sum(1 for kw in expected_keywords if kw in lowered)
    coverage = covered / len(expected_keywords) if expected_keywords else 0.0
    words = len(text.split())
    length_bonus = 0.5 if words > 60 else 0.0
    return max(1.0, min(5.0, 1.0 + 3.5 * coverage + length_bonus))


def mean_absolute_error(pairs):
    """Mean |judge - human| over (judge, human) pairs."""
    return sum(abs(j - h) for j, h in pairs) / len(pairs)


def pearson(xs, ys):
    """Pearson correlation, pure Python; 0.0 when undefined."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) *
                    sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def main():
    print("Judge vs synthetic human labels (rubric: keyword coverage")
    print("+ 0.5 length bonus over 60 words):")
    pairs = []
    for sample in SAMPLES:
        score = judge_score(sample["text"])
        pairs.append((score, sample["human"]))
        print(f"  {sample['id']:>12}: judge {score:.2f}  human "
              f"{sample['human']}  diff {abs(score - sample['human']):.2f}")
    judges = [j for j, _ in pairs]
    humans = [h for _, h in pairs]
    print(f"  mean absolute error: {mean_absolute_error(pairs):.3f}")
    print(f"  correlation: {pearson(judges, humans):.3f}")
    print()
    print("Verbosity-bias check: same content, padded with filler.")
    concise = SAMPLES[0]["text"]
    padded = concise + " " + FILLER
    print(f"  concise ({len(concise.split())} words): "
          f"judge {judge_score(concise):.2f}, human 5")
    print(f"  padded  ({len(padded.split())} words): "
          f"judge {judge_score(padded):.2f}, human 5 (same content)")
    print("  -> the judge rewards the longer answer although a human "
          "rates the content equal. That is verbosity bias: a judge "
          "habit to measure and correct, not a property of quality.")
    print()
    print("Judge limitations to carry into real systems: a judge cannot")
    print("verify facts it does not know, it inherits its own model's")
    print("biases, and it agrees with humans most where the rubric is")
    print("sharpest — vague rubrics produce confident-looking noise.")


if __name__ == "__main__":
    main()
