# -*- coding: utf-8 -*-
"""anime_ekaya "Midnight Channel" slide renderer.

Mechanism copied from trend-signals-social/scripts/render_html (deck JSON ->
per-slide HTML -> headless Chromium @2x -> LANCZOS -> 1080x1350 PNG); visual
system is anime_ekaya's own (night indigo / neon coral / lavender, Space
Grotesk + Inter + Archivo Black). See income-engine/docs/anime_ekaya-strategy.md
section 8.

Usage:  py -3 render.py decks/<deck>.json [--out <dir>]

Slide roles: hook, rank (numbered rows w/ notes), pick (one rec per slide),
principle, closer. Rich text: [[...]] -> coral highlight, **...** -> medium.
"""
import argparse
import html as htmllib
import io
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONT_DIR = "file:///" + (HERE / "fonts").as_posix()
W, H = 1080, 1350
DSF = 2

CSS = """
@font-face { font-family:'Space Grotesk'; src:url('__FONTDIR__/SpaceGrotesk-Bold.ttf'); font-weight:700; }
@font-face { font-family:'Inter'; src:url('__FONTDIR__/Inter-Regular.ttf'); font-weight:400; }
@font-face { font-family:'Inter'; src:url('__FONTDIR__/Inter-Medium.ttf'); font-weight:500; }
@font-face { font-family:'Archivo Black'; src:url('__FONTDIR__/ArchivoBlack-Regular.ttf'); font-weight:400; }

:root {
  --bg:#131022; --panel:#1C1834; --paper:#F3F0FF; --coral:#FF5D73;
  --lav:#9D8DF1; --muted:#A9A3C2; --hair:#37315A;
}
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1350px; }
body.slide {
  background:var(--bg); color:var(--paper);
  font-family:'Inter',sans-serif; font-kerning:normal;
  display:flex; flex-direction:column; padding:64px 72px 56px;
  position:relative; overflow:hidden;
}
/* faint scanline texture band, brand motif */
body.slide::before {
  content:""; position:absolute; left:0; right:0; top:0; height:6px;
  background:linear-gradient(90deg, var(--coral) 0 38%, var(--lav) 38% 62%, var(--hair) 62% 100%);
}
.brandrow { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:56px; }
.wordmark { font-family:'Space Grotesk'; font-weight:700; font-size:34px; letter-spacing:.08em; color:var(--coral); }
.wordmark .jp { font-family:'Yu Gothic','Meiryo',sans-serif; font-size:26px; color:var(--lav); letter-spacing:.18em; margin-left:14px; }
.kicker { font-size:24px; font-weight:500; letter-spacing:.22em; text-transform:uppercase; color:var(--muted); }
.content { flex:1; display:flex; flex-direction:column; justify-content:center; }
.footrow { display:flex; justify-content:space-between; font-size:23px; font-weight:500;
  letter-spacing:.2em; text-transform:uppercase; color:var(--muted); margin-top:48px; }
mark { background:none; color:var(--coral); }
strong { font-weight:500; }

.display { font-family:'Space Grotesk'; font-weight:700; font-size:96px; line-height:1.06;
  letter-spacing:-0.015em; }
.dek { font-size:40px; line-height:1.42; color:var(--muted); margin-top:44px; max-width:880px; }

/* rank rows */
.heading { font-family:'Space Grotesk'; font-weight:700; font-size:58px; line-height:1.1; margin-bottom:52px; }
ol.rows { list-style:none; }
ol.rows li { display:flex; gap:34px; padding:34px 0; border-top:2px solid var(--hair); align-items:flex-start; }
ol.rows li:last-child { border-bottom:2px solid var(--hair); }
.rk { font-family:'Archivo Black'; font-size:56px; line-height:1.05; color:var(--coral); min-width:96px; }
.rt { flex:1; }
.rt .title { font-family:'Space Grotesk'; font-weight:700; font-size:44px; line-height:1.14; }
.rt .note { font-size:30px; line-height:1.4; color:var(--muted); margin-top:10px; }

/* pick card */
.picknum { font-family:'Archivo Black'; font-size:130px; line-height:1; color:var(--coral); }
.picktitle { font-family:'Space Grotesk'; font-weight:700; font-size:72px; line-height:1.08; margin-top:34px; }
.pickwhy { font-size:42px; line-height:1.45; margin-top:44px; max-width:900px; }
.pickmeta { display:inline-block; font-size:27px; font-weight:500; letter-spacing:.14em;
  text-transform:uppercase; color:var(--lav); border:2px solid var(--hair);
  padding:16px 26px; border-radius:999px; margin-top:56px; }

/* principle */
.plabel { font-size:26px; font-weight:500; letter-spacing:.22em; text-transform:uppercase;
  color:var(--lav); display:block; margin-bottom:40px; }
.pbody { font-size:42px; line-height:1.45; color:var(--muted); margin-top:44px; max-width:900px; }

/* closer */
.handle { display:inline-block; font-family:'Space Grotesk'; font-weight:700; font-size:40px;
  color:#131022; background:var(--coral); padding:20px 36px; border-radius:16px; margin-top:56px; }
"""

CSS = CSS.replace("__FONTDIR__", FONT_DIR)


def esc(s):
    return htmllib.escape(s, quote=False)


def rich(s):
    s = esc(s)
    while "[[" in s and "]]" in s:
        s = s.replace("[[", "<mark>", 1).replace("]]", "</mark>", 1)
    while s.count("**") >= 2:
        s = s.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    return s


def role_hook(sl):
    dek = f'<p class="dek">{rich(sl["dek"])}</p>' if sl.get("dek") else ""
    return f'<h1 class="display">{rich(sl["h"])}</h1>{dek}'


def role_rank(sl):
    rows = "".join(
        f'<li><span class="rk">{esc(it["n"])}</span><span class="rt">'
        f'<span class="title">{rich(it["title"])}</span>'
        + (f'<span class="note" style="display:block">{rich(it["note"])}</span>' if it.get("note") else "")
        + "</span></li>"
        for it in sl["items"]
    )
    return f'<h2 class="heading">{rich(sl["h"])}</h2><ol class="rows">{rows}</ol>'


def role_pick(sl):
    return (f'<div class="picknum">{esc(sl["n"])}</div>'
            f'<h2 class="picktitle">{rich(sl["title"])}</h2>'
            f'<p class="pickwhy">{rich(sl["why"])}</p>'
            f'<span class="pickmeta">{esc(sl["meta"])}</span>')


def role_principle(sl):
    lbl = f'<span class="plabel">{esc(sl["label"])}</span>' if sl.get("label") else ""
    body = "".join(f'<p class="pbody">{rich(p)}</p>' for p in sl.get("body", []))
    return f'{lbl}<h2 class="display" style="font-size:76px">{rich(sl["h"])}</h2>{body}'


def role_closer(sl):
    body = f'<p class="dek">{rich(sl["body"])}</p>' if sl.get("body") else ""
    handle = f'<span class="handle">{esc(sl["handle"])}</span>' if sl.get("handle") else ""
    return f'<h1 class="display">{rich(sl["h"])}</h1>{body}{handle}'


ROLES = {"hook": role_hook, "rank": role_rank, "pick": role_pick,
         "principle": role_principle, "closer": role_closer}


def slide_html(deck, sl, page_no, total):
    inner = ROLES[sl["role"]](sl)
    kicker = sl.get("kicker", deck.get("kicker", ""))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body class="slide">
<header class="brandrow"><span class="wordmark">EKAYA<span class="jp">エカヤ</span></span><span class="kicker">{esc(kicker)}</span></header>
<main class="content">{inner}</main>
<footer class="footrow"><span>YOUR NEXT ANIME, SORTED</span><span>{page_no}/{total}</span></footer>
</body></html>"""


def render_deck(deck_path, out_dir=None):
    deck = json.loads(Path(deck_path).read_text(encoding="utf-8"))
    slug = deck["slug"]
    out = Path(out_dir) if out_dir else HERE / "out" / slug
    out.mkdir(parents=True, exist_ok=True)
    html_dir = out / "_html"
    html_dir.mkdir(exist_ok=True)
    prev_dir = out / "_preview350"
    prev_dir.mkdir(exist_ok=True)
    total = len(deck["slides"])

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=DSF)
        for i, sl in enumerate(deck["slides"], 1):
            doc = slide_html(deck, sl, i, total)
            hpath = html_dir / f"slide-{i}.html"
            hpath.write_text(doc, encoding="utf-8")
            page.goto(hpath.as_uri())
            page.wait_for_function("document.fonts.status === 'loaded'")
            img = Image.open(io.BytesIO(page.screenshot()))
            assert img.size == (W * DSF, H * DSF), f"unexpected raster {img.size}"
            img = img.convert("RGB").resize((W, H), Image.LANCZOS)
            img.save(out / f"slide-{i}.png")
            img.resize((350, 438), Image.LANCZOS).save(prev_dir / f"slide-{i}.png")
            print(f"  slide-{i}.png  ({sl['role']})")
        browser.close()
    print(f"OK: {total} slides -> {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--out")
    args = ap.parse_args()
    render_deck(args.deck, args.out)
