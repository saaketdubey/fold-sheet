#!/usr/bin/env python3
"""Ritual fold-sheet generator (landscape Letter, panels side by side, dashed fold line, binding gutter).

Usage:  python3 fold_sheet.py spec.json out.pdf [--proof]
        --proof ignores "imposition" and renders the panels in reading order (for checking content).
Fonts:  expects ./fonts/fontsource-noto-sans-<version> and ./fonts/fontsource-noto-sans-devanagari-<version>
        next to this script (see README setup).

Spec (JSON):
{
  "title": "Sheet title (default for every panel)",
  "footer": ["line", ...],            # default footer for every panel ([] = none; for the once-per-page key, set [] here and put the key in each left panel's own footer)
  "panels_per_page": 2,               # optional; >2 panels flow onto extra pages
  "imposition": "none",               # optional; "booklet" = duplex saddle-stitch sheet order (panels_per_page 2;
                                      #   panel count padded to a multiple of 4 with blank panels at the end)
  "folio": true,                      # optional; page numbers at the outer bottom corner of every panel with content
  "css": "extra CSS overrides",       # optional, appended last
  "panels": [
    { "title": "...", "subtitle": "...", "footer": [...],     # all optional overrides
      "folio": false,                                        # optional; skip the page number on this panel (e.g. a title page)
      "units": [                                             # Sanskrit/Greek unit format
        {"label": "SOURCE LABEL (optional)", "cls": "grk (optional, for Greek script)",
         "dev": "script line", "iast": "plain transliteration", "phon": "pronunciation", "en": "English"}
      ],
      "prose_html": "<p>...</p>"                              # or free prose (stanzas, rituals)
    }
  ]
}
Prints "OVERFLOW (panel index, px)" if any panel's content doesn't fit (index = position in the spec). Fix before delivering.
"""
import asyncio, html, json, pathlib, sys
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
F = HERE / "fonts"

CSS = """
@page { size: 11in 8.5in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; }
body { font-family: 'Noto Sans', 'Noto Sans Devanagari', sans-serif; color: #1b1b1b; }
.page { width: 11in; height: 8.5in; display: flex; break-after: page; }
.page:last-child { break-after: auto; }
.panel { flex: 1; width: 5.5in; padding: 0.55in 0.55in 0.45in; display: flex; flex-direction: column; overflow: hidden; }
.panel + .panel { border-left: 1px dashed #9a9a9a; }
.panel.L { padding-right: 0.75in; }   /* binding gutter: he staples on the fold */
.panel.R { padding-left: 0.75in; }
h1 { font-size: 18pt; font-weight: 700; margin: 0 0 3pt; letter-spacing: -0.005em; }
.sub { font-size: 9.5pt; color: #555; margin-bottom: 16pt; }
/* unit format */
.lbl { font-size: 8pt; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #666; margin: 2pt 0 4pt; }
.u + .lbl { margin-top: 8pt; }
.u { margin-bottom: 14pt; }
.dev { font-family: 'Noto Sans Devanagari', sans-serif; font-size: 20pt; font-weight: 500; line-height: 1.45; margin-bottom: 1pt; }
.dev.grk { font-family: 'Noto Sans', sans-serif; font-weight: 400; }
.iast { font-style: italic; font-size: 11pt; color: #333; margin-bottom: 1pt; }
.phon { font-size: 11pt; letter-spacing: 0.01em; margin-bottom: 2pt; }
.en { font-size: 11pt; color: #333; }
/* prose format */
.prose { font-size: 11pt; line-height: 1.75; color: #1b1b1b; }
.prose p { margin: 0 0 14pt; }
.prose .skt { font-family: 'Noto Sans Devanagari', sans-serif; }   /* inline Devanagari, same size as text */
.prose .tr { font-style: italic; color: #444; }                    /* transliteration */
.prose .ph { color: #333; }                                         /* pronunciation */
.nw { white-space: nowrap; }                                        /* wrap each pronunciation word: no mid-word breaks */
.prose .h2 { font-size: 8pt; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #666; margin: 4pt 0 5pt; }
.prose .stage { font-style: italic; color: #555; font-size: 0.85em; line-height: 1.4; }   /* ritual instructions */
.prose .vox { margin: 6pt 0 6pt 14pt; letter-spacing: 0.05em; }                          /* barbarous names, own line */
.prose .gk { margin: 8pt 0 1pt; } .prose .gl { color: #555; font-size: 0.9em; margin: 0 0 4pt 14pt; }  /* line + gloss */
/* page number: outer bottom corner */
.panel { position: relative; }
.folio { position: absolute; bottom: 0.28in; font-size: 8pt; color: #888; }
.panel.L .folio { left: 0.5in; }
.panel.R .folio { right: 0.5in; }
/* footer */
.foot { margin-top: auto; border-top: 0.75pt solid #999; padding-top: 6pt; font-size: 8pt; color: #555; line-height: 1.45; }
.foot p { margin: 0; }
"""

def _font_dir(name):
    """Find ./fonts/fontsource-<name>-<any version>/ so an npm version bump doesn't break the setup."""
    prefix = f"fontsource-{name}-"
    hits = sorted(d for d in F.glob(prefix + "*") if d.is_dir() and d.name[len(prefix):len(prefix)+1].isdigit())
    if not hits:
        sys.exit(f"fonts/fontsource-{name}-<version>/ not found next to this script; see README setup")
    return hits[-1]

FONT_CSS = [_font_dir("noto-sans") / f for f in ("400.css", "400-italic.css", "700.css")] + \
           [_font_dir("noto-sans-devanagari") / f for f in ("400.css", "500.css")]

def impose(count, mode, n):
    """Spec panel indices in print order; None = blank panel (padded at the end, last resort)."""
    if mode == "booklet":
        if n != 2:
            sys.exit("booklet imposition needs panels_per_page 2")
        total = -(-count // 4) * 4
        if total != count:
            print(f"NOTE: padded {count} panels to {total} for booklet (blank panels at the end); rebalance if possible")
        idx = list(range(count)) + [None] * (total - count)
        order = []
        for s in range(total // 4):          # sheet s: front = last | first, back = second | second-last
            lo, hi = 2 * s, total - 1 - 2 * s
            order += [idx[hi], idx[lo], idx[lo + 1], idx[hi - 1]]
        return order
    total = -(-count // n) * n
    return list(range(count)) + [None] * (total - count)

def build_html(spec):
    e = html.escape
    n = spec.get("panels_per_page", 2)
    links = "".join(f'<link rel="stylesheet" href="{p.as_uri()}">' for p in FONT_CSS)
    order = impose(len(spec["panels"]), spec.get("imposition", "none"), n)
    panels = []
    for pos, i in enumerate(order):
        side = "L" if pos % n == 0 else ("R" if pos % n == n - 1 else "")
        if i is None:
            panels.append(f'<section class="panel {side}"></section>')
            continue
        p = spec["panels"][i]
        foot = "".join(f"<p>{e(x)}</p>" for x in p.get("footer", spec.get("footer", [])))
        units = "".join(
            (f'<div class="lbl">{e(u["label"])}</div>' if u.get("label") else "")
            + f'<div class="u"><div class="dev {u.get("cls", "")}">{e(u["dev"])}</div>'
            + (f'<div class="iast">{e(u["iast"])}</div>' if u.get("iast") else "")
            + (f'<div class="phon">{e(u["phon"])}</div>' if u.get("phon") else "")
            + f'<div class="en">{e(u["en"])}</div></div>'
            for u in p.get("units", []))
        prose = f'<div class="prose">{p["prose_html"]}</div>' if p.get("prose_html") else ""
        has_content = bool(p.get("units") or p.get("prose_html"))
        folio = f'<div class="folio">{i + 1}</div>' if has_content and p.get("folio", spec.get("folio", True)) else ""
        panels.append(f'<section class="panel {side}"><h1>{e(p.get("title", spec.get("title", "")))}</h1>'
                      f'<div class="sub">{e(p.get("subtitle", ""))}</div>{units}{prose}'
                      + (f'<div class="foot">{foot}</div>' if foot else "") + folio + "</section>")
    pages = "".join(f'<div class="page">{"".join(panels[i:i+n])}</div>' for i in range(0, len(panels), n))
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8">{links}'
            f'<style>{CSS}{spec.get("css", "")}</style></head><body>{pages}</body></html>'), order

async def render(spec, out):
    src = HERE / "_sheet.html"   # temp file beside the script, not in the outputs folder
    html_out, order = build_html(spec)
    src.write_text(html_out, encoding="utf-8")
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        await pg.goto(src.as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        over = await pg.evaluate("[...document.querySelectorAll('.panel')]"
                                 ".map((p,i)=>[i, p.scrollHeight - p.clientHeight]).filter(x=>x[1]>1)")
        if over:
            print("OVERFLOW (panel index, px):", [(order[i], px) for i, px in over])
        await pg.pdf(path=out, width="11in", height="8.5in", print_background=True)
        await b.close()
    src.unlink()

if __name__ == "__main__":
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    if "--proof" in sys.argv:
        spec["imposition"] = "none"
    asyncio.run(render(spec, sys.argv[2]))
