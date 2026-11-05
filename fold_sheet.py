#!/usr/bin/env python3
"""Ritual fold-sheet generator (landscape Letter, panels side by side, dashed fold line, binding gutter).

Usage:  python3 fold_sheet.py spec.json out.pdf
Fonts:  expects ./fonts/fontsource-noto-sans-5.3.0 and ./fonts/fontsource-noto-sans-devanagari-5.3.0
        next to this script (see SKILL.md setup).

Spec (JSON):
{
  "title": "Sheet title (default for every panel)",
  "footer": ["line", ...],            # default footer for every panel ([] = none; for the once-per-page key, set [] here and put the key in each left panel's own footer)
  "panels_per_page": 2,               # optional; >2 panels flow onto extra pages
  "css": "extra CSS overrides",       # optional, appended last
  "panels": [
    { "title": "...", "subtitle": "...", "footer": [...],     # all optional overrides
      "units": [                                             # Sanskrit/Greek unit format
        {"label": "SOURCE LABEL (optional)", "cls": "grk (optional, for Greek script)",
         "dev": "script line", "iast": "plain transliteration", "phon": "pronunciation", "en": "English"}
      ],
      "prose_html": "<p>...</p>"                              # or free prose (stanzas, rituals)
    }
  ]
}
Prints "OVERFLOW (panel index, px)" if any panel's content doesn't fit. Fix before delivering.
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
/* footer */
.foot { margin-top: auto; border-top: 0.75pt solid #999; padding-top: 6pt; font-size: 8pt; color: #555; line-height: 1.45; }
.foot p { margin: 0; }
"""

FONT_CSS = ["fontsource-noto-sans-5.3.0/400.css", "fontsource-noto-sans-5.3.0/400-italic.css",
            "fontsource-noto-sans-5.3.0/700.css",
            "fontsource-noto-sans-devanagari-5.3.0/400.css", "fontsource-noto-sans-devanagari-5.3.0/500.css"]

def build_html(spec):
    e = html.escape
    n = spec.get("panels_per_page", 2)
    links = "".join(f'<link rel="stylesheet" href="{(F / p).as_uri()}">' for p in FONT_CSS)
    panels = []
    for i, p in enumerate(spec["panels"]):
        side = "L" if i % n == 0 else ("R" if i % n == n - 1 else "")
        foot = "".join(f"<p>{e(x)}</p>" for x in p.get("footer", spec.get("footer", [])))
        units = "".join(
            (f'<div class="lbl">{e(u["label"])}</div>' if u.get("label") else "")
            + f'<div class="u"><div class="dev {u.get("cls", "")}">{e(u["dev"])}</div>'
            + (f'<div class="iast">{e(u["iast"])}</div>' if u.get("iast") else "")
            + (f'<div class="phon">{e(u["phon"])}</div>' if u.get("phon") else "")
            + f'<div class="en">{e(u["en"])}</div></div>'
            for u in p.get("units", []))
        prose = f'<div class="prose">{p["prose_html"]}</div>' if p.get("prose_html") else ""
        panels.append(f'<section class="panel {side}"><h1>{e(p.get("title", spec.get("title", "")))}</h1>'
                      f'<div class="sub">{e(p.get("subtitle", ""))}</div>{units}{prose}'
                      + (f'<div class="foot">{foot}</div>' if foot else "") + "</section>")
    if len(panels) % n:   # last resort only: rebalance first so no panel is blank
        panels += ['<section class="panel R"></section>'] * (n - len(panels) % n)
    pages = "".join(f'<div class="page">{"".join(panels[i:i+n])}</div>' for i in range(0, len(panels), n))
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8">{links}'
            f'<style>{CSS}{spec.get("css", "")}</style></head><body>{pages}</body></html>')

async def render(spec, out):
    src = HERE / "_sheet.html"   # temp file beside the script, not in the outputs folder
    src.write_text(build_html(spec), encoding="utf-8")
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page()
        await pg.goto(src.as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        over = await pg.evaluate("[...document.querySelectorAll('.panel')]"
                                 ".map((p,i)=>[i, p.scrollHeight - p.clientHeight]).filter(x=>x[1]>1)")
        if over:
            print("OVERFLOW (panel index, px):", over)
        await pg.pdf(path=out, width="11in", height="8.5in", print_background=True)
        await b.close()
    src.unlink()

if __name__ == "__main__":
    asyncio.run(render(json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")), sys.argv[2]))
