# classical-gloss

A [Claude Code](https://claude.com/claude-code) skill for locating the original-language primary source of a classical/ancient text (Greek, Latin, etc.) and building word-by-word interlinear ("trilinear") glosses of specific passages — original-language line, transliteration, short gloss, aligned in monospace.

It isn't tied to any one author: the underlying method (skip the JavaScript-rendered Perseus reading interfaces, pull the raw TEI XML that PerseusDL publishes on GitHub instead, verify citations against the inline milestone tags, gloss every word rather than a single lifted term) works for any Perseus-hosted Greek or Latin text — Homer, Plato, Thucydides, Cicero, Virgil, Aristotle, and the rest of the canonical corpus PerseusDL hosts.

## Install

Drop this directory into your Claude Code skills folder (typically `~/.claude/skills/`):

```bash
git clone git@github.com:<you>/classical-gloss.git ~/.claude/skills/classical-gloss
```

## What's here

- `SKILL.md` — the workflow Claude follows: locate the source, verify the passage and its citation, segment and gloss every word, align the columns, format the result.
- `scripts/align_interlinear.py` — computes column widths for the interlinear block instead of hand-spacing them (which reliably drifts as soon as word lengths vary).
- `references/perseus-sources.md` — which Perseus entry points return real text vs. which only render through JavaScript, and how to find a text's file on PerseusDL's GitHub if you don't already have its URN.

See `SKILL.md` for the full workflow and a worked example.
