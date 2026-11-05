# fold-sheet

Printable fold-sheets for mantras, hymns and prayers: landscape Letter, two panels per page, a dashed fold line down the middle, a binding gutter so the sheet can be stapled on the fold. You write a small JSON spec; the script renders a PDF.

**Authorship:** I wrote the specification, the layout conventions and the verification steps. The Python was written by an AI assistant (Claude) to that spec and checked by me against printed output. The example text is Rigveda 10.125, which is in the public domain; the English translation is original to this repo.

## The problem

I print short sacred texts for use at a home altar. Every version I tried — word-processor tables, web printouts, PDFs from other tools — broke on the same points: Devanagari rendered without proper conjuncts, no room for a staple, no consistent place for a pronunciation key, and no way to reproduce the layout for the next text without starting over.

## What it does

- Lays out each text as reading units: **Devanagari → plain transliteration → pronunciation respelling → English**, one unit per line of verse.
- Holds a 0.75 in clear gutter on both sides of the fold line so the sheet can be stapled.
- Prints the pronunciation key once per page, not once per panel.
- Reports `OVERFLOW` if any panel's content doesn't fit, so nothing silently gets clipped.
- Also handles plain prose panels (introductions, prayers, translations) in the same layout.

## Spec in, PDF out

Input — one panel from [`examples/devi_sukta_spec.json`](examples/devi_sukta_spec.json):

```json
{
  "subtitle": "Rigveda 10.125 | Verse 1",
  "units": [
    {"dev": "अहं रुद्रेभिर्वसुभिश्चरामि",
     "iast": "aham rudrebhir vasubhish charami",
     "phon": "a-ham rud-RAY-bhir va-su-bhish cha-RAA-mi",
     "en": "I move with the Rudras and the Vasus,"}
  ]
}
```

Output — [`examples/devi_sukta.pdf`](examples/devi_sukta.pdf): 10 panels across 5 pages. Page 1 is an introduction to the hymn, pages 1–5 carry the eight verses, and the last panel is the full English.

## Run it

```bash
pip install -r requirements.txt
playwright install chromium

# fonts (Noto Sans + Noto Sans Devanagari) via npm, next to the script
mkdir -p fonts && cd fonts
npm pack @fontsource/noto-sans @fontsource/noto-sans-devanagari
for f in *.tgz; do d=${f%.tgz}; mkdir -p $d && tar xzf $f -C $d --strip-components=1; done
cd ..

python3 fold_sheet.py examples/devi_sukta_spec.json devi_sukta.pdf
```

The script prints nothing on success. If it prints `OVERFLOW (panel index, px)`, that panel has too much content — split it or trim the spacing in the spec's `css` field.

The example spec was generated from a verse table by [`examples/make_spec.py`](examples/make_spec.py), which is the easier way to build a multi-verse sheet.

## Conventions

The layout and text rules the generator follows — gutter, unit format, how the pronunciation line marks long vowels, English capitalisation — are in [`docs/conventions.md`](docs/conventions.md). That document is the actual product; the script is the part that enforces it.

## What I learned

- **Specify the constraints, not the code.** The gutter width, the once-per-page key and the overflow check all came from printed drafts that failed. Writing them down as rules was the work; the code followed.
- **Verify the content, not just the layout.** The Devanagari was checked against an online Rigveda text and the metre attribution against the traditional viniyoga before the sheet was built. A clean PDF of a wrong text is still wrong.
- **Resolve sandhi at unit breaks and say so.** Splitting a verse into padas means some words that run together in the manuscript get separated. The sheet's footer discloses this rather than hiding it.
