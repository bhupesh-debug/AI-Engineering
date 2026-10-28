"""Entropy and perplexity on a toy corpus.

Illustrative demo only. The corpus below is synthetic, invented for
teaching — it is not data from any real model or book. Entropy measures
how unpredictable a probability distribution is (in bits); perplexity
is 2 ** entropy, and reads as "how many equally likely options the
model is effectively choosing between."

Plain-language idea: imagine a bag of marbles. If the bag holds only red
marbles, you are never surprised — entropy 0. If it holds red and blue
in equal numbers, every draw is a coin flip — entropy 1 bit. Perplexity
turns that surprise into a head-count: a perplexity of 4 means the model
is about as uncertain as if it were choosing between 4 equal options.
"""

import math
import re
from collections import Counter

# Synthetic toy corpus, invented for this demo.
TOY_CORPUS = [
    "the cat sat on the mat",
    "the dog sat on the rug",
    "the cat chased the dog",
    "a bird sat on the roof",
]


def tokenize(text):
    """Lowercase words made of letters and digits."""
    return re.findall(r"[a-z0-9]+", text.lower())


def unigram_distribution(sentences):
    """Return (probabilities, total_token_count) for a unigram model."""
    counts = Counter()
    for sentence in sentences:
        counts.update(tokenize(sentence))
    total = sum(counts.values())
    probs = {word: count / total for word, count in counts.items()}
    return probs, total


def entropy_of_distribution(probs):
    """Shannon entropy in bits; zero-probability outcomes add nothing."""
    return -sum(p * math.log2(p) for p in probs if p > 0.0)


def perplexity_from_entropy(entropy_bits):
    """Perplexity is 2 raised to the entropy in bits."""
    return 2.0 ** entropy_bits


def sentence_perplexity(sentence, probs, total_tokens):
    """Perplexity of a sentence under the unigram model.

    Uses a simple add-one smoothing rule (a teaching version): every
    known word gets (count + 1) / (total + vocab_size), and an unseen
    word gets 1 / (total + vocab_size). Lower perplexity means the
    sentence looks more like the corpus; higher means more surprising.
    """
    vocab_size = len(probs)
    denom = total_tokens + vocab_size
    log_sum = 0.0
    words = tokenize(sentence)
    for word in words:
        p = (probs.get(word, 0.0) * total_tokens + 1.0) / denom
        log_sum += math.log2(p)
    avg_log = log_sum / len(words)
    return 2.0 ** (-avg_log)


def ascii_bars(pairs, width=40):
    """Tiny bar chart: list of (label, value) -> text lines."""
    top = max(value for _, value in pairs) or 1.0
    lines = []
    for label, value in pairs:
        bar = "#" * max(1, int(round(value / top * width)))
        lines.append(f"{label:>12} | {bar} {value:.3f}")
    return "\n".join(lines)


def main():
    probs, total = unigram_distribution(TOY_CORPUS)
    entropy = entropy_of_distribution(list(probs.values()))
    print("Toy corpus (synthetic, 4 sentences, "
          f"{total} tokens, {len(probs)} distinct words)")
    print()
    print("Most common words and their probabilities:")
    print(ascii_bars(sorted(probs.items(), key=lambda kv: -kv[1])[:8]))
    print()
    print(f"Distribution entropy: {entropy:.3f} bits")
    print(f"Distribution perplexity: {perplexity_from_entropy(entropy):.3f}")
    print("  -> the model is about as uncertain as choosing between "
          f"{perplexity_from_entropy(entropy):.1f} equal options.")
    print()
    typical = "the cat sat on the mat"
    odd = "quantum banana orbits zebra"
    print(f"Perplexity of a typical sentence ('{typical}'): "
          f"{sentence_perplexity(typical, probs, total):.2f}")
    print(f"Perplexity of a surprising sentence ('{odd}'): "
          f"{sentence_perplexity(odd, probs, total):.2f}")
    print("  -> the surprising sentence scores much higher, which is "
          "exactly what perplexity is for: spotting text the model "
          "finds unlikely.")


if __name__ == "__main__":
    main()
