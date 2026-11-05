# Fold-sheet conventions

These are the rules every sheet follows. `fold_sheet.py` enforces the layout ones; the text ones are applied when writing the spec.

## Layout

- Landscape Letter (11 × 8.5 in), two panels per page, separated by a dashed vertical fold line.
- Sheets are printed single-sided and stapled along the fold, so each panel keeps a **0.75 in binding gutter** on its fold side and ~0.5 in on the outer edge. Nothing sits in the gutter, and it is never shrunk to make content fit.
- Each panel: bold title → small grey subtitle → content → optional thin rule and footer.
- Continuation panels repeat the title with the subtitle "…, continued".
- One work is one PDF, however many pages. Pages are not scarce: prefer adding a page to cramming, and don't leave the last panel blank — rebalance at a natural seam (a verse or section boundary) instead.
- The pronunciation key prints **once per page**, on the left panel, not on every panel.
- Sans-serif type (Noto Sans + Noto Sans Devanagari). Devanagari must render with proper conjuncts.
- Body text around 11 pt. Rebalance panels before shrinking type.

## Sheet type A — Sanskrit unit sheet

The text is split into reading units (typically one pada, or half-verse, each). Every unit stacks four lines:

1. **Devanagari**, large.
2. **Plain transliteration**, italic, no diacritics: `vishnuh prachyam sthitash chakri`, not `viṣṇuḥ prācyāṃ sthitaś cakrī`.
3. **Pronunciation respelling**, hyphenated by syllable. Capitals mark **long-vowel syllables only** (aa, ee, oo, ay, oh, ai, ow): "hold this vowel", not stress — Sanskrit has no stress. `vish-nuh PRAA-CHYAAM sthi-tash-chak-REE`.
4. **English translation.**

Rules:

- One verse per panel where the verse fits. If a panel holds several short mantras, each gets a small uppercase source label above it.
- Subtitle format: `Source ch.verse | Verse n`.
- Punctuation at the end of the English line mirrors the Sanskrit: semicolon at । (half-verse), full stop at ॥ (verse end), commas elsewhere. Keep । and ॥ in the Devanagari, `|` / `||` in the transliteration.
- Translate close to the Sanskrit: keep each word's English in the same unit as the word; carry one verb across units only where the Sanskrit does. Proper names stay names (Narasimha, not "Man-Lion"); gloss only epithets the text itself translates.
- Where a unit break falls inside a sandhi-joined word, resolve the sandhi at the break so no unit starts mid-word, and say so in the footer.
- Standard Sanskrit footer, four lines:
  1. `a = u in but; i = sit; u = put. AA = father; EE = see; OO = food; OH = go; AY = say; AI = eye; OW = cow. Capitals mark long vowels: hold them. Sanskrit has no stress.`
  2. `ri (as in hri, dhri, pri) = one quick syllable. kh / chh / th / dh / bh = the consonant + a puff of air (th is never English "th"). Final h = a soft breath echoing the vowel before it. gny (for jn) is often gy in North Indian usage.`
  3. Per-sheet notes, ending "Sanskrit split into reading units." Vedic texts add "Vedic pitch accents are not marked."
  4. Per-sheet source line.

## Sheet type B — prose sheet

For introductions, prayers, translations and other running text.

- Plain paragraphs, everything one size (~11 pt). Non-Latin script the same size as the English.
- A few Sanskrit words inside English prose go inline as Devanagari with the transliteration in parentheses; no unit breakdown.
- Greek, where used: Koine pronunciation (β = v, δ = dh, η/ι/υ/ει/οι = ee, αι = eh, ευ = ev/ef, initial h silent). For Greek the capitals mark the **stressed** syllable, and the page footer says so. Each pronunciation word is wrapped so it never breaks across a line.

## English conventions

- Capitalise divine kinship terms and pronouns for deities (Mother, Father, You, Them, Who), weapons, the five elements (Earth, Water, Fire, Air, Space) and Sky.
- Vocative is written "O'" ("O' Goddess").
- ṛta → "Rta".
- Transcribe source texts exactly. Typos and inconsistencies in a source are listed for a decision, never silently fixed.

## Workflow

1. Read the source completely and transcribe exactly.
2. Verify before building: check the text against an online edition where possible, and note what was and wasn't verified. Never invent citations.
3. Propose the layout (panel count, what goes where, what is left out) before producing anything.
4. Build, render, and look at every page: balance, gutter, footer placement, ugly wraps, near-empty panels. The generator must print no `OVERFLOW`.
5. Deliver one PDF with a short list of what changed and anything still open.

## Spec format

```json
{
  "title": "Default title for every panel",
  "footer": [],
  "panels_per_page": 2,
  "css": "optional CSS overrides, appended last",
  "panels": [
    {
      "title": "optional override",
      "subtitle": "Source | Verse n",
      "footer": ["key line 1", "key line 2"],
      "units": [
        {"label": "OPTIONAL SOURCE LABEL", "dev": "…", "iast": "…", "phon": "…", "en": "…"}
      ],
      "prose_html": "<p>…</p>  (instead of units, for prose panels)"
    }
  ]
}
```

Set the top-level `footer` to `[]` and give the key to each left-hand (even-indexed) panel's own `footer` to get the once-per-page key.
