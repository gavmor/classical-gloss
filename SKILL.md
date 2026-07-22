---
name: classical-gloss
description: Locate the original-language primary source for a classical/ancient text (Greek, Latin, etc.) and build word-by-word interlinear ("trilinear") glosses of specific passages -- Greek/Latin line, transliteration, short gloss, aligned in monospace. Use this whenever the user asks to find "the original Greek/Latin," the "untranslated text," or wants a passage "glossed," "interlinear," or "trilinear," especially while working in a wiki, notes, or commentary about an ancient author (Aristotle, Plato, Homer, the New Testament, etc.). Also trigger when the user wants to verify a scholarly citation (Bekker/Stephanus/Loeb/Bekker-line number) against the actual source rather than from memory, or wants etymology grounded in the real inflected word that appears in a passage rather than a dictionary citation form. Don't wait for the user to say "Perseus" or name a specific corpus -- any request to see, quote, or align the underlying ancient-language text for something already being discussed in English should route here.
---

# Interlinear Gloss

Two things this skill does, almost always together: (1) find the actual primary-source text in its original language, since most classical texts are public domain and have their critical editions freely available online, and (2) turn a passage from it into a proper word-by-word gloss — not a single lifted term with an etymology note attached, but every word of the sentence, aligned so a reader can follow the original language, its transliteration, and its meaning in lockstep.

## Why full-sentence, word-by-word matters

It's tempting to pull out one etymologically interesting word from a passage — the headline term — and build a nice little breakdown of *just that word*, leaving the rest of the sentence as an English paraphrase. This under-delivers on what a gloss is for. A single word's etymology is useful, but it's not a *passage* gloss — the reader can't actually follow the Greek/Latin against the argument, and worse, it's easy to accidentally cite the word's dictionary/lemma form (nominative singular, present tense, etc.) instead of the actual inflected form that appears in the sentence, which breaks the one promise an interlinear gloss makes: *this is what's really there*. Cover every word, including function words like conjunctions and articles — they're short, and skipping them is what turns a gloss into a highlight reel.

## Step 1: Locate the primary source

Read `references/perseus-sources.md` before searching — it lists which Perseus entry points return real text via a normal fetch and which ones only render through JavaScript (and will waste your time if you don't know that going in). The short version: skip Scaife/Hopper/PhiloLogic/Logeion for raw text access, and go straight to the plain TEI XML PerseusDL publishes on GitHub (`canonical-greekLit` or `canonical-latinLit`), which fetches cleanly because it's static XML, not an app.

Download the file once to a stable local path (not a throwaway temp file that disappears at the end of the session) so you can grep it repeatedly without re-fetching. If the text runs to hundreds of KB across ten books, that's fine — you'll only ever read small slices of it via grep, never the whole thing at once.

## Step 2: Find and verify the exact passage

The XML is usually one giant line per paragraph or chapter, with citation markers threaded through as inline `<milestone>` tags. Reading the raw file with a line-oriented tool won't work — a single `grep -n` hit can be an unreadable wall of text spanning an entire chapter. Use bounded-context extraction instead:

```bash
grep -oP ".{150}GREEKWORD.{150}" source.xml
```

This gets you a readable window around a real match instead of the whole paragraph. Once you've found the sentence, confirm its citation — don't guess it from memory, even for a passage you're confident you recognize. Find the line number of the match, then look at the milestone tags on or immediately before that line:

```bash
grep -n "GREEKWORD" source.xml                              # -> line number N
sed -n '(N-2),(N)p' source.xml | grep -oP 'milestone unit="page" resp="[^"]+" n="[0-9]+[ab]"'
```

Whatever citation scheme the milestones use (Bekker page/line for Aristotle, Stephanus pages for Plato, book/line for verse), only cite what you actually saw in the tags. A citation that "sounds right" but wasn't checked this way is exactly the kind of error that's invisible until someone tries to look the passage up and it's off by a few lines.

## Step 3: Segment every word and gloss it

Walk the sentence word by word, in order — every word gets a column, including articles, particles, and conjunctions. For each word, work out:

- **Transliteration** — a plain-alphabet rendering
- **A short gloss** — a lexical translation (1-3 words) or, for function words and grammatical machinery, a terse tag (`NOM`, `GEN.PL`, `ACC`, `PTCP`, `MOD`, `PTCL`, etc.). Keep every gloss short; a long explanatory gloss is what makes columns balloon and forces the free translation into the wrong place. Save the fuller explanation for the prose note underneath the block.

Watch specifically for the citation-form trap: if the sentence uses a genitive plural, gloss the genitive plural, and say so — don't quietly substitute the word's nominative singular dictionary form because that's the "cleaner" one to explain etymology on. If a form's morphology is worth unpacking (a compound, a privative, a recognizable suffix), do that unpacking on the form that's actually in the sentence, cross-referencing the citation form only if it helps ("the actual genitive-plural form here, not the citation form X").

## Step 4: Generate the ngloss block

We use the [Obsidian Interlinear Glossing](https://github.com/mijyuoon/obsidian-ling-gloss) plugin's `ngloss` alternative syntax. This syntax uses brackets rather than manual space-padding, making it robust against word length variations and much easier to read and write. Use the bundled script to generate it from your data:

```bash
echo '[["μετὰ","meta","after"],["δὲ","de","and"],["ταῦτα","tauta","these.ACC"]]' \
  | python3 scripts/align_interlinear.py
```

It takes a JSON array of words, each word an array of tier-strings (Greek, transliteration, gloss — or more tiers if you want them), and formats them into the `\gl` command structure where each primary word is followed by bracketed tiers.

## Step 5: Format the result

One aligned block per full sentence — not broken into many small 4-5 word chunks. The `ngloss` block handles wrapping natively.

The shape, worked from an actual passage (Aristotle, *Nicomachean Ethics* VII.1, Bekker 1145a25-27):

```markdown
### Bk. VII, ch. 1 (Bekker 1145a25-27)

\`\`\`ngloss
\ex καὶ γὰρ ὥσπερ οὐδὲ θηρίου ἐστὶ κακία οὐδʼ ἀρετή, οὕτως οὐδὲ θεοῦ, ἀλλʼ ἣ μὲν τιμιώτερον ἀρετῆς, ἣ δʼ ἕτερόν τι γένος κακίας.
\gl καὶ [kai] [for]
    γὰρ [gar] [indeed]
    ὥσπερ [hōsper] [just-as]
    οὐδὲ [oude] [not-even]
    θηρίου [thēriou] [beast.GEN]
    ἐστὶ [esti] [is]
    κακία [kakia] [vice]
    οὐδʼ [oud'] [nor]
    ἀρετή, [aretē] [virtue]
    οὕτως [houtōs] [so]
    οὐδὲ [oude] [not-even]
    θεοῦ, [theou] [god.GEN]
    ἀλλʼ [all'] [but]
    ἣ [hē] [the-one]
    μὲν [men] [PTCL]
    τιμιώτερον [timiōteron] [more-honorable]
    ἀρετῆς, [aretēs] [virtue.GEN]
    ἣ [hē] [the-other]
    δʼ [d'] [and]
    ἕτερόν [heteron] [different.ACC]
    τι [ti] [a-certain]
    γένος [genos] [kind.ACC]
    κακίας. [kakias] [vice.GEN]
\ft For just as there is neither vice nor virtue belonging to a beast, so too none belonging to a god — but the one state is more honorable than virtue, and the other a different kind from vice.
\`\`\`

[one or two sentences tying a key word's morphology back to whatever point this passage is being cited for]
```

The pattern: citation heading, one ngloss block containing the original text (`\ex`), the gloss (`\gl`), and the translation (`\ft`), followed by prose connecting it to whatever surrounding argument or claim it's grounding.

## Step 6: Audio Embedding (Optional but Recommended)

When compiling a new gloss block, if you have access to the `/speak-greek` skill, you should use its "Export Mode" to generate an audio file for the passage. Save the file to `assets/audio/<citation>.mp3` (e.g., `assets/audio/1145a25.mp3`), and embed it right above the `ngloss` block like this:

```markdown
![[1145a25.mp3]]

\`\`\`ngloss
...
```
## A note on copyright

The ancient text itself and its standard critical edition (Bekker, Bywater, Stephanus, OCT, Loeb Greek/Latin, etc.) are all long out of copyright — quote them as fully and freely as the passage requires. If there's also a modern in-copyright translation sitting alongside it (a named 20th/21st-century translator's English rendering), don't quote that at length; a short phrase here and there is fine, but paraphrase the rest in your own words. The gloss you're building *is* the translation for the purposes of this exercise — that's the whole point of doing it word by word instead of leaning on someone else's finished sentence.

## Exhaustive Citation (Bulk Extraction / Map-Reduce)

When the user asks to extract *all* occurrences of a specific concept/word from the entire corpus (e.g., "Pull each of the 122 occurrences into this note"), do NOT attempt to parse the entire XML or generate the glosses in a single agent session. This will exceed context limits and corrupt the formatting. Instead, use the built-in Map-Reduce workflow:

### 1. Extract and Chunk targets
Run the bundled `extract_tei_targets.py` script to pull all sentences matching the target word/regex from the TEI XML into JSON chunks. This script preserves the exact Bekker/Stephanus line numbers.

```bash
python3 ~/.gemini/skills/classical-gloss/scripts/extract_tei_targets.py \
  --xml references/nicomachean-ethics-greek.xml \
  --pattern 'πρ[αάᾶ]ξ[ιε][\p{L}\p{M}]*' \
  --chunk-size 10 \
  --out-prefix chunk_targets
```

### 2. Dispatch Parallel Subagents
Invoke parallel subagents (one for each JSON chunk). **CRITICAL:** You must explicitly instruct every subagent to format their outputs exactly as `ngloss` bracketed blocks (using the example from Step 5) and to write their output to `out_chunk_N.md`. Do not trust subagents to remember the format without strict instructions or providing them with the `align_interlinear.py` script.

### 3. Assemble and Append
Once all subagents finish, use the bundled `assemble_glosses.py` to safely concatenate their markdown outputs and append them directly to the target file. This bypasses your own context window limits and avoids hallucination.

```bash
python3 ~/.gemini/skills/classical-gloss/scripts/assemble_glosses.py \
  --chunks 'out_chunk_*.md' \
  --target concepts/target_file.md \
  --heading 'Exhaustive Citations'
```
