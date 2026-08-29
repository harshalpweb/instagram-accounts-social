# -*- coding: utf-8 -*-
"""Hype Tingle deck renderer: deck JSON -> HTML -> headless Chromium ->
1080x1350 PNG (rendered at device_scale_factor=2, LANCZOS-downsampled)
plus 350px feed-scale previews. Mechanism follows the proven
trend-signals-social/scripts/render_html pattern; visual system is Hype
Tingle's own (see accounts/hype_tingles/tools/template.css).

Usage:  py -3 render.py decks/<deck>.json [--out <dir>]
Output: <out>/<slug>/slide-N.png  +  <out>/<slug>/_preview350/
"""
import argparse
import html as htmllib
import json
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONT_DIR = "file:///" + (HERE.parent / "brand" / "fonts").as_posix()
CSS = (HERE / "template.css").read_text(encoding="utf-8").replace("__FONTDIR__", FONT_DIR)

W, H = 1080, 1350
DSF = 2


def esc(s):
    return htmllib.escape(s, quote=False)


def rich(s):
    """[[...]] -> volt highlight span, {{...}} -> pink span."""
    s = esc(s)
    while "[[" in s and "]]" in s:
        s = s.replace("[[", '<span class="hl">', 1).replace("]]", "</span>", 1)
    while "{{" in s and "}}" in s:
        s = s.replace("{{", '<span class="hp">', 1).replace("}}", "</span>", 1)
    while s.count("**") >= 2:
        s = s.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    return s


def role_hook(sl):
    kicker = f'<span class="hook-kicker">{esc(sl.get("kicker", "WELCOME TO HYPE TINGLE"))}</span>'
    dek = f'<p class="dek">{rich(sl["dek"])}</p>' if sl.get("dek") else ""
    tease = f'<p class="tease">{rich(sl["tease"])}</p>' if sl.get("tease") else ""
    return f'{kicker}<h1 class="display">{rich(sl["h"])}</h1>{dek}{tease}', ""


def role_speaker(sl):
    cls = "quote big" if sl.get("big") else "quote"
    sub = f'<p class="sub">{rich(sl["sub"])}</p>' if sl.get("sub") else ""
    inner = (
        f'<div class="avatar">{sl["animal"]}</div>'
        f'<span class="namechip">{esc(sl["name"])}</span>'
        f'<h1 class="{cls}">{rich(sl["quote"])}</h1>{sub}'
    )
    return inner, ("volt" if sl.get("payoff") else "")


def role_review(sl):
    n = int(sl.get("stars", 1))
    stars = '<span>' + "★" * n + '</span><span class="off">' + "★" * (5 - n) + "</span>"
    inner = (
        '<div class="card">'
        f'<div class="rev-head"><div class="rev-avatar">{sl["animal"]}</div>'
        f'<div><div class="rev-name">{esc(sl["name"])}</div>'
        f'<div class="rev-verified">{esc(sl.get("meta", "Verified animal"))}</div></div></div>'
        f'<div class="stars">{stars}</div>'
        f'<div class="rev-title">{rich(sl["title"])}</div>'
        f'<p class="rev-body">{rich(sl["body"])}</p>'
        "</div>"
    )
    return inner, ("volt" if sl.get("payoff") else "")


def role_guide(sl):
    num = f'<div class="stepnum">{esc(str(sl["num"]))}</div>' if sl.get("num") is not None else ""
    body = f'<p class="guide-body">{rich(sl["body"])}</p>' if sl.get("body") else ""
    return f'{num}<h2 class="guide-h">{rich(sl["h"])}</h2>{body}', ("volt" if sl.get("payoff") else "")


def role_closer(sl):
    body = f'<p class="dek">{rich(sl["body"])}</p>' if sl.get("body") else ""
    handle = f'<span class="handle">{esc(sl.get("handle", "@hype_tingles"))}</span>'
    return f'<h1 class="display">{rich(sl["h"])}</h1>{body}{handle}', sl.get("theme", "")


ROLES = {
    "hook": role_hook,
    "speaker": role_speaker,
    "review": role_review,
    "guide": role_guide,
    "closer": role_closer,
}


def build_html(deck, i, sl, total):
    inner, body_cls = ROLES[sl["role"]](sl)
    last = i == total
    cue = "" if last else '<span class="cue">Keep swiping &#8594;</span>'
    if last:
        cue = '<span class="cue">Follow for more</span>'
    eptag = esc(deck.get("episode", ""))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body class="{body_cls}">
<div class="topbar"><span class="wordmark">HYPE&nbsp;<span class="tingle">TINGLE</span></span><span class="eptag">{eptag}</span></div>
<main>{inner}</main>
<div class="botbar">{cue}<span class="counter">{i}/{total}</span></div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    deck = json.loads(Path(args.deck).read_text(encoding="utf-8"))
    slug = deck["slug"]
    out = Path(args.out) if args.out else HERE / "out" / slug
    (out / "_preview350").mkdir(parents=True, exist_ok=True)
    (out / "_html").mkdir(parents=True, exist_ok=True)

    total = len(deck["slides"])
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": W, "height": H}, device_scale_factor=DSF
        )
        for i, sl in enumerate(deck["slides"], 1):
            doc = build_html(deck, i, sl, total)
            hpath = out / "_html" / f"slide-{i}.html"
            hpath.write_text(doc, encoding="utf-8")
            page.goto("file:///" + hpath.resolve().as_posix())
            page.wait_for_function("document.fonts.ready.then(() => true)")
            loaded = page.evaluate(
                "document.fonts.check('20px \"Archivo Black\"') && document.fonts.check('20px \"Space Grotesk\"')"
            )
            if not loaded:
                print(f"WARNING slide-{i}: brand fonts did not load", file=sys.stderr)
            page.wait_for_timeout(120)
            raw = out / f"slide-{i}.raw.png"
            page.screenshot(path=str(raw))
            img = Image.open(raw).convert("RGB")
            img = img.resize((W, H), Image.LANCZOS)
            img.save(out / f"slide-{i}.png")
            img.resize((350, 438), Image.LANCZOS).save(
                out / "_preview350" / f"slide-{i}.png"
            )
            raw.unlink()
            print(f"slide-{i}.png ok")
        browser.close()
    print(f"deck '{slug}': {total} slides -> {out}")


if __name__ == "__main__":
    main()
