# -*- coding: utf-8 -*-
"""Nuvarel deck renderer: deck JSON -> per-slide HTML -> headless Chromium
(1080x1350 @ device_scale_factor=2) -> LANCZOS downsample -> PNG.

Same mechanism as trend-signals-social/scripts/render_html (the proven
HTML/Playwright pattern), own code and own brand (see
docs/nuvarel-strategy.md section 8 for the locked visual identity).

Usage:
    py -3 render_nuvarel.py decks/<deck>.json [--out <dir>]

Deck JSON: {"slug": str, "series": str, "slides": [{role, ...}, ...]}
Roles: hook, swatch, principle, verdict, closer, photo.
Rich text: **...** -> <strong>, //...// -> <em>.

photo role (photoreal pivot, strategy §8 rev. 2026-09-05, Group CTO):
    {"role": "photo", "src": "<png, repo-relative or absolute>",
     "layout": "full" | "matted", "key": "dark" | "mid" | "light",
     "eyebrow": "The Evidence · No. 01", "h": "<= 7 words>",
     "silent": false, "index": "72"}
  - src is cover-cropped to exactly 1080x1350 before compositing.
  - silent: true renders the photograph alone, no type, no meta row -- the
    strategy requires frame 2 of every carousel to be one of these.
  - index (optional): the Nuvarel Index numeral in the corner.
  - photo slides carry no footer bar; the renderer writes
    <out>/_photo_meta.json (type coverage, headline words, luminance) which
    gate_check.py reads for the photo-aware checks.

Fonts load from Google Fonts (Cormorant Garamond + Archivo, both OFL);
the script waits on document.fonts.ready before screenshotting.
"""
import argparse
import base64
import html as htmllib
import io
import json
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
CSS = (HERE / "template.css").read_text(encoding="utf-8")
W, H = 1080, 1350
DSF = 2
PHOTO_MAX_WORDS = 7

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600'
    '&family=Archivo:wght@400;500;600&display=block" rel="stylesheet">'
)

# Bounding-box area of every type element on a photo slide, as a fraction
# of the frame -- the strategy's "<=15% of frame" rule, measured in-page.
COVERAGE_JS = """
() => {
  const els = document.querySelectorAll('.meta-row span, .display, .rule, .index');
  let area = 0;
  for (const e of els) { const r = e.getBoundingClientRect(); area += r.width * r.height; }
  return area / (1080 * 1350);
}
"""


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


def photo_data_uri(src):
    """Load the photograph, cover-crop it to exactly 1080x1350, return a
    data URI. Resolves repo-relative paths against the repo root."""
    p = Path(src)
    if not p.is_absolute() and not p.exists():
        p = REPO_ROOT / src
    if not p.exists():
        raise FileNotFoundError(f"photo src not found: {src}")
    img = Image.open(p).convert("RGB")
    if img.size != (W, H):
        sw, sh = img.size
        scale = max(W / sw, H / sh)
        img = img.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
        left = (img.width - W) // 2
        top = (img.height - H) // 2
        img = img.crop((left, top, left + W, top + H))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def photo_html(deck, sl):
    """Photo slide: its own document shape (no <main>, no footer bar)."""
    uri = photo_data_uri(sl["src"])
    layout = sl.get("layout", "full")
    silent = bool(sl.get("silent"))
    eyebrow = esc(sl.get("eyebrow", deck.get("series", "")))
    words = 0 if silent else len(sl.get("h", "").split())
    if not silent and words == 0:
        raise ValueError("photo slide needs an 'h' headline unless silent: true")
    if words > PHOTO_MAX_WORDS:
        raise ValueError(
            f"photo slide headline is {words} words; max {PHOTO_MAX_WORDS} "
            f"(strategy §8 typography restraint): {sl.get('h')!r}"
        )
    index = (
        f'<div class="index">{esc(str(sl["index"]))}</div>' if sl.get("index") else ""
    )
    meta_row = (
        f'<div class="meta-row"><span>{eyebrow}</span>'
        f'<span class="wordmark">Nuvarel</span></div>'
    )
    caption = (
        f'<div class="caption"><hr class="rule">'
        f'<h1 class="display">{rich(sl["h"])}</h1></div>'
    ) if not silent else ""

    if layout == "matted":
        cls = "matted silent" if silent else "matted"
        body = (
            f'<body class="{cls}">{"" if silent else meta_row}'
            f'<div class="frame" style="background-image:url(\'{uri}\')"></div>'
            f'{caption}{"" if silent else index}</body>'
        )
    else:
        scrims = "" if silent else '<div class="scrim"></div><div class="scrim-top"></div>'
        body = (
            f'<body class="photo dark">'
            f'<div class="bg" style="background-image:url(\'{uri}\')"></div>'
            f'{scrims}{"" if silent else meta_row}{caption}{"" if silent else index}</body>'
        )
    doc = (
        f'<!doctype html><html><head><meta charset="utf-8">{FONT_LINK}'
        f'<style>{CSS}</style></head>{body}</html>'
    )
    meta = {
        "layout": layout, "key": sl.get("key"), "silent": silent,
        "headline_words": words, "src": sl["src"],
    }
    return doc, meta


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
    photo_meta = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": W, "height": H}, device_scale_factor=DSF
        )
        for i, sl in enumerate(deck["slides"], 1):
            is_photo = sl["role"] == "photo"
            if is_photo:
                doc, meta = photo_html(deck, sl)
            else:
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
            if is_photo:
                meta["type_coverage"] = round(page.evaluate(COVERAGE_JS), 4)
                lum = sum(img.convert("L").getdata()) / (W * H) / 255
                meta["mean_luminance"] = round(lum, 3)
                photo_meta[f"slide-{i}"] = meta
                print(f"  slide-{i}.png  photo/{meta['layout']} key={meta['key']} "
                      f"words={meta['headline_words']} type={meta['type_coverage']:.1%} "
                      f"lum={lum:.2f}")
            else:
                print(f"  slide-{i}.png")
        browser.close()
    if photo_meta:
        (out_dir / "_photo_meta.json").write_text(
            json.dumps(photo_meta, indent=2), encoding="utf-8"
        )
    print(f"OK {slug}: {total} slides -> {out_dir}")


if __name__ == "__main__":
    sys.exit(main())
