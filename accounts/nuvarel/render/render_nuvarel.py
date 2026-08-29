# -*- coding: utf-8 -*-
"""Nuvarel deck renderer: deck JSON -> per-slide HTML -> headless Chromium
(1080x1350 @ device_scale_factor=2) -> LANCZOS downsample -> PNG.

Same mechanism as trend-signals-social/scripts/render_html (the proven
HTML/Playwright pattern), own code and own brand (see
docs/nuvarel-strategy.md section 8 for the locked visual identity).

Usage:
    py -3 render_nuvarel.py decks/<deck>.json [--out <dir>]

Deck JSON: {"slug": str, "series": str, "slides": [{role, ...}, ...]}
Roles: hook, swatch, principle, verdict, closer.
Rich text: **...** -> <strong>, //...// -> <em>.

Fonts load from Google Fonts (Cormorant Garamond + Archivo, both OFL);
the script waits on document.fonts.ready before screenshotting.
"""
import argparse
import html as htmllib
import json
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
CSS = (HERE / "template.css").read_text(encoding="utf-8")
W, H = 1080, 1350
DSF = 2

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600'
    '&family=Archivo:wght@400;500;600&display=block" rel="stylesheet">'
)


def esc(s):
    return htmllib.escape(s, quote=False)


def rich(s):
    s = esc(s)
    while s.count("**") >= 2:
        s = s.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    while s.count("//") >= 2:
        s = s.replace("//", "<em>", 1).replace("//", "</em>", 1)
    return s


def luminance(hexcolor):
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def role_hook(sl):
    dek = f'<p class="dek">{rich(sl["dek"])}</p>' if sl.get("dek") else ""
    return (
        f'<h1 class="display">{rich(sl["h"])}</h1>'
        f'<hr class="rule">{dek}'
    ), "hook"


def role_swatch(sl):
    hexcode = sl["hex"].upper()
    text_on_swatch = "#F2EEE6" if luminance(hexcode) < 0.45 else "#2A241E"
    body = f'<p class="body">{rich(sl["body"])}</p>' if sl.get("body") else ""
    return (
        f'<div class="swatch-block" style="background:{hexcode}">'
        f'<span class="hex" style="color:{text_on_swatch}">{hexcode}</span></div>'
        f'<h2 class="headline swatch-name">{rich(sl["name"])}</h2>'
        f'<p class="swatch-role">{esc(sl["role_line"])}</p>{body}'
    ), "swatch"


def role_principle(sl):
    lbl = f'<span class="klabel">{esc(sl["klabel"])}</span>' if sl.get("klabel") else ""
    body = "".join(f'<p class="body">{rich(p)}</p>' for p in sl.get("body", []))
    rule = '<hr class="rule">' if body else ""
    return f'{lbl}<h2 class="headline">{rich(sl["h"])}</h2>{rule}{body}', "principle"


def role_verdict(sl):
    kind = sl["kind"]  # "splurge" | "skip"
    body = "".join(f'<p class="body">{rich(p)}</p>' for p in sl.get("body", []))
    return (
        f'<span class="verdict-tag {kind}">{esc(kind)}</span>'
        f'<h2 class="headline">{rich(sl["h"])}</h2>'
        f'<hr class="rule">{body}'
    ), "verdict"


def role_closer(sl):
    handle = f'<p class="handle">{esc(sl.get("handle", "@nuvarel_"))}</p>'
    return (
        f'<h1 class="display">{rich(sl["h"])}</h1>'
        f'<hr class="rule">{handle}'
    ), "closer dark"


BUILDERS = {
    "hook": role_hook,
    "swatch": role_swatch,
    "principle": role_principle,
    "verdict": role_verdict,
    "closer": role_closer,
}


def slide_html(deck, sl, idx, total):
    inner, body_class = BUILDERS[sl["role"]](sl)
    if sl.get("theme") == "dark" and "dark" not in body_class:
        body_class += " dark"
    series = esc(deck.get("series", ""))
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONT_LINK}
<style>{CSS}</style></head>
<body class="{body_class}">
<div class="meta-row"><span>{series}</span><span class="wordmark">Nuvarel</span></div>
<main>{inner}</main>
<div class="footer"><span>@nuvarel_</span><span>{idx:02d} / {total:02d}</span></div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    deck = json.loads(Path(args.deck).read_text(encoding="utf-8"))
    slug = deck["slug"]
    out_dir = Path(args.out) if args.out else HERE / "out" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    html_dir = out_dir / "_html"
    html_dir.mkdir(exist_ok=True)

    total = len(deck["slides"])
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": W, "height": H}, device_scale_factor=DSF
        )
        for i, sl in enumerate(deck["slides"], 1):
            doc = slide_html(deck, sl, i, total)
            (html_dir / f"slide-{i}.html").write_text(doc, encoding="utf-8")
            page.set_content(doc, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(150)
            raw = out_dir / f"slide-{i}-raw.png"
            page.screenshot(path=str(raw))
            img = Image.open(raw)
            img = img.resize((W, H), Image.LANCZOS)
            img.save(out_dir / f"slide-{i}.png")
            raw.unlink()
            print(f"  slide-{i}.png")
        browser.close()
    print(f"OK {slug}: {total} slides -> {out_dir}")


if __name__ == "__main__":
    sys.exit(main())
