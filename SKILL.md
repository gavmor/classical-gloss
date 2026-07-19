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

## Step 4: Align it — compute this, don't hand-space it

Manually padding columns with spaces looks fine for the first two or three words and then silently drifts as soon as word lengths vary — a four-letter word next to a twelve-letter gloss throws off every column after it. Use the bundled script instead of eyeballing it:

```bash
echo '[["μετὰ","meta","after"],["δὲ","de","and"],["ταῦτα","tauta","these.ACC"]]' \
  | python3 scripts/align_interlinear.py
```

It takes a JSON array of words, each word an array of tier-strings (Greek, transliteration, gloss — or more tiers if you want them), and pads each word's own column to fit its longest tier, then joins columns with two spaces. Read the output before using it; if something still looks off, check whether a tier string contains characters that legitimately widen a column (this is expected, not a bug).

## Step 5: Format the result

One aligned block per full sentence — not broken into many small 4-5 word chunks. Long lines that run wide are fine and preferred; a reader following an interlinear gloss expects to scan a whole sentence across, not hunt through a dozen small tables. Use a plain code fence, not a markdown table — tables force artificial cell-wrapping and don't preserve the monospace alignment the columns depend on.

The shape, worked from an actual passage (Aristotle, *Nicomachean Ethics* VII.1, Bekker 1145a25-27):

```markdown
### Bk. VII, ch. 1 (Bekker 1145a25-27)

> καὶ γὰρ ὥσπερ οὐδὲ θηρίου ἐστὶ κακία οὐδʼ ἀρετή, οὕτως οὐδὲ θεοῦ, ἀλλʼ ἣ μὲν τιμιώτερον ἀρετῆς, ἣ δʼ ἕτερόν τι γένος κακίας.

\`\`\`
καὶ  γὰρ     ὥσπερ    οὐδὲ      θηρίου     ἐστὶ  κακία  οὐδʼ  ἀρετή   οὕτως   οὐδὲ      θεοῦ     ἀλλʼ  ἣ        μὲν   τιμιώτερον      ἀρετῆς      ἣ          δʼ   ἕτερόν         τι         γένος     κακίας
kai  gar     hōsper   oude      thēriou    esti  kakia  oud'  aretē   houtōs  oude      theou    all'  hē       men   timiōteron      aretēs      hē         d'   heteron        ti         genos     kakias
for  indeed  just-as  not-even  beast.GEN  is    vice   nor   virtue  so      not-even  god.GEN  but   the-one  PTCL  more-honorable  virtue.GEN  the-other  and  different.ACC  a-certain  kind.ACC  vice.GEN
\`\`\`

*"For just as there is neither vice nor virtue belonging to a beast, so too none belonging to a god — but the one state is more honorable than virtue, and the other a different kind from vice."* [one or two sentences tying a key word's morphology back to whatever point this passage is being cited for]
```

The pattern: citation heading, blockquote of the full original-language sentence, one aligned block, then an italicized free translation followed by prose (not another table) connecting it to whatever surrounding argument or claim it's grounding.

## A note on copyright

The ancient text itself and its standard critical edition (Bekker, Bywater, Stephanus, OCT, Loeb Greek/Latin, etc.) are all long out of copyright — quote them as fully and freely as the passage requires. If there's also a modern in-copyright translation sitting alongside it (a named 20th/21st-century translator's English rendering), don't quote that at length; a short phrase here and there is fine, but paraphrase the rest in your own words. The gloss you're building *is* the translation for the purposes of this exercise — that's the whole point of doing it word by word instead of leaning on someone else's finished sentence.

## Doing this at scale

If several passages or several pages need glossing, this parallelizes cleanly: each passage's citation-verification and word segmentation is independent of every other passage, so one subagent per page (or per passage, for a very long page) works well, as long as each one gets the same local source-file path and the same method above rather than being told to search the web fresh each time. Give each one the worked example from Step 5 as a template to match, not just a description of the format — that's what actually keeps 20+ parallel outputs consistent with each other.
