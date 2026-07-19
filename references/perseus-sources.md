# Finding primary-source classical texts online

Most public-domain Greek and Latin texts (anything edited before ~1928, which covers nearly all standard critical editions of ancient authors) live in the Perseus Digital Library ecosystem. This note is about *which* Perseus entry points actually hand you raw text vs. which ones look promising but won't.

## Dead ends (confirmed by direct testing, don't waste a turn on these)

These all render their actual text via JavaScript. `WebFetch` converts static HTML to markdown, so it only ever sees the surrounding app shell — never the Greek/Latin itself, no matter how the prompt is phrased:

- **Scaife Viewer** (`scaife.perseus.org`) — Perseus's current reading platform
- **Perseus Hopper** (`perseus.tufts.edu/hopper/text?doc=...`) — the classic interface, including its per-word morphology popups
- **Perseus under PhiloLogic** (`perseus.uchicago.edu`) — a University of Chicago mirror with a different search UI, same problem
- **Logeion** (`logeion.uchicago.edu`) — word-lookup dictionary tool, also JS-rendered

If you try one of these and the fetch comes back describing only navigation links, headers, or "Browse Library" / "Text Search" — that's this problem, not a fluke. Don't retry with a different prompt; switch approaches instead.

## The reliable path: PerseusDL's raw TEI XML on GitHub

Perseus's actual text data is open-licensed (CC-BY-SA) and sits as plain TEI XML in two repos:

- **Greek texts**: `github.com/PerseusDL/canonical-greekLit`
- **Latin texts**: `github.com/PerseusDL/canonical-latinLit`

Each work's file path follows the pattern `data/<textgroup>/<work>/<textgroup>.<work>.<version>.xml`, where the textgroup/work numbers come from the **CTS URN** (Canonical Text Services identifier) Perseus assigns to that text — e.g. Aristotle's *Nicomachean Ethics* is `urn:cts:greekLit:tlg0086.tlg010`, so its file is `data/tlg0086/tlg010/tlg0086.tlg010.perseus-grc2.xml`.

**To find the URN/file for a text you don't already know:**
1. Search the Perseus Catalog (`catalog.perseus.org`) or just web-search `"<author> <work>" perseus catalog urn:cts` — the catalog page names the exact edition (e.g. Bekker 1831, Bywater 1894) and its URN.
2. Or search directly: `github PerseusDL canonical-greekLit <textgroup-or-work-number>` (or `canonical-latinLit` for Latin).
3. Fetch the raw file with a normal `curl`/`WebFetch` against `raw.githubusercontent.com/PerseusDL/<repo>/master/<path>` — this is plain XML, not JS-rendered, so it comes through cleanly.

Download it once into a stable local file (not a session-only scratch path) so repeated greps across a whole gloss-writing session — or a future session — don't re-fetch it. If you're working inside a wiki/vault that already tracks its sources (e.g. a `.manifest.json`), register the GitHub URL as a source there too, same as any other ingested document.

## Reading the citation scheme

The XML encodes the standard scholarly citation (Bekker numbers for Aristotle, Stephanus pages for Plato, book/line for verse authors, etc.) as inline `<milestone>` tags threaded through the text, e.g.:

```xml
<milestone unit="page" resp="Bekker" n="1130b"/>
<milestone unit="line" resp="Bekker" n="25"/>
```

The specific `unit=` and `resp=` values vary by author/edition — grep a small stretch of the file for `<milestone` to see which scheme a given text uses before assuming it's Bekker-style. Once you know the pattern, the citation for any passage you find is just "whichever milestone tag appears immediately before it" — see the main SKILL.md for the exact grep recipe.
