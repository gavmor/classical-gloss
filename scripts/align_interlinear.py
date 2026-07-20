#!/usr/bin/env python3
"""Format an interlinear gloss using the ngloss alternative syntax.

Input (stdin): a JSON array of "words". Each word is itself an array of
strings, one per tier, in the order you want them printed top-to-bottom
(commonly [greek, transliteration, gloss], but any number of tiers works).

  [["μετὰ", "meta", "after"], ["δὲ", "de", "and"], ["ταῦτα", "tauta", "these.ACC"]]

Output (stdout): the ngloss block ready to drop inside a \gl command.
Each word gets its own line, with the primary word followed by bracketed tiers.

Usage:
    echo '[["μετὰ","meta","after"],["δὲ","de","and"]]' | python3 scripts/align_interlinear.py
    python3 scripts/align_interlinear.py < words.json
"""
import json
import sys


def format_ngloss(rows):
    if not rows:
        return ""
    
    out_lines = []
    for i, word in enumerate(rows):
        if not word:
            continue
        
        # First word has \gl, others are indented
        prefix = "\\gl " if i == 0 else "    "
        
        primary = word[0]
        # Wrap subsequent tiers in brackets
        bracketed = " ".join(f"[{tier}]" for tier in word[1:])
        
        line = f"{prefix}{primary} {bracketed}"
        out_lines.append(line)
        
    return "\n".join(out_lines)


def main():
    data = json.load(sys.stdin)
    if not isinstance(data, list):
        print("Input must be a JSON array of [tier1, tier2, ...] word arrays.", file=sys.stderr)
        sys.exit(1)
    print(format_ngloss(data))


if __name__ == "__main__":
    main()
