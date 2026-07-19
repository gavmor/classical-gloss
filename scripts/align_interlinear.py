#!/usr/bin/env python3
"""Pad an interlinear gloss so every tier lines up in a monospace font.

Why this exists: hand-spacing columns reliably drifts out of alignment the
moment word lengths vary within a line (a 4-letter Greek word next to a
12-letter gloss). Computing the width per word-column, instead of eyeballing
spaces, is cheap and always correct.

Input (stdin): a JSON array of "words". Each word is itself an array of
strings, one per tier, in the order you want them printed top-to-bottom
(commonly [greek, transliteration, gloss], but any number of tiers works).

  [["μετὰ", "meta", "after"], ["δὲ", "de", "and"], ["ταῦτα", "tauta", "these.ACC"]]

Output (stdout): the aligned block, one line per tier, ready to drop inside
a ``` fence. Columns are separated by two spaces.

Usage:
    echo '[["μετὰ","meta","after"],["δὲ","de","and"]]' | python3 align_interlinear.py
    python3 align_interlinear.py < words.json
"""
import json
import sys


def align(rows):
    if not rows:
        return ""
    n_tiers = len(rows[0])
    if any(len(word) != n_tiers for word in rows):
        raise ValueError("every word must have the same number of tiers")
    # Width PER WORD-COLUMN = max length across that word's own tiers.
    # (Not a single width shared across the whole tier/row -- that produces
    # staggered, misaligned output, because a long gloss on one word would
    # force every OTHER word's Greek/transliteration line to pad way out.)
    col_widths = [max(len(tier) for tier in word) for word in rows]
    out_lines = []
    for t in range(n_tiers):
        line = "  ".join(word[t].ljust(col_widths[i]) for i, word in enumerate(rows))
        out_lines.append(line.rstrip())
    return "\n".join(out_lines)


def main():
    data = json.load(sys.stdin)
    if not isinstance(data, list):
        print("Input must be a JSON array of [tier1, tier2, ...] word arrays.", file=sys.stderr)
        sys.exit(1)
    print(align(data))


if __name__ == "__main__":
    main()
