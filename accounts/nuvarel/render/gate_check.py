# -*- coding: utf-8 -*-
"""Nuvarel render gate: mechanical checks + feed-scale previews.

Checks per slide PNG in a rendered deck dir:
  1. exact 1080x1350 dimensions;
  2. ink coverage (fraction of pixels differing from the slide's modal
     background color by >40/255 in any channel) inside a 2-60% band:
     below = an empty/failed render, above = visual mud at feed scale.
     Swatch slides carry large color fields, hence the wide top of the
     band vs. text-only systems. **Skipped on photo slides** -- a
     photograph has no modal background, so the number is meaningless
     there (spike finding 4, 2026-09-05);
  3. writes 350px-wide previews to <dir>/_preview350/ ;
  4. swatch differentiation (added 2026-09-01 after a CCO-caught defect:
     two near-identical swatches and one swatch invisible on its own
     ground shipped to review): if ../decks/<slug>.json exists, every
     pair of swatch hexes must be >= MIN_SWATCH_DIST apart (Euclidean
     RGB), and each swatch must be >= MIN_SWATCH_DIST from its own
     slide ground (espresso if the slide is theme "dark", alabaster
     otherwise). Ink-vs-background alone cannot see this class;
  5. photo-aware checks (added 2026-09-05, Group CTO, photoreal pivot),
     driven by the deck JSON + <dir>/_photo_meta.json the renderer wrote:
       - every photo slide declares a tonal key (dark/mid/light) and its
         rendered mean luminance must land in that key's band -- this is
         the strategy's tonal-rotation rule made checkable;
       - type coverage <= 15% of frame; headline <= 7 words; a silent
         slide has zero type;
       - in any deck containing photo slides, slide 2 must be a silent
         photo (strategy §8: "frame 2 of every carousel is a full-bleed
         photograph with no type at all").

Viewing the previews is still a mandatory human/agent step; the numbers
do not replace eyes (same doctrine as trend-signals-social's gate) -- and
on photo slides specifically, ~1/3 of generated frames carry a shadow or
geometry artifact that NO check here can see. Look at every frame.

Usage: py -3 gate_check.py out/<slug>
"""
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

from PIL import Image

BAND = (0.02, 0.60)
MIN_SWATCH_DIST = 25.0
ALABASTER = (0xF2, 0xEE, 0xE6)
ESPRESSO = (0x2A, 0x24, 0x1E)

# Mean-luminance bands per declared key. Anchors from the 2026-09-05 spike:
# full-bleed dark frames measured 0.146-0.168, a matted mid frame 0.504.
# "light" is unproven in generation yet; its band is the strategy's intent.
KEY_BANDS = {"dark": (0.0, 0.34), "mid": (0.34, 0.62), "light": (0.62, 1.0)}
PHOTO_MAX_TYPE = 0.15
PHOTO_MAX_WORDS = 7


def _rgb(hexcode):
    h = hexcode.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def _load_deck(deck_dir: Path):
    deck_path = deck_dir.parent.parent / "decks" / f"{deck_dir.name}.json"
    if not deck_path.exists():
        return None
    return json.loads(deck_path.read_text(encoding="utf-8"))


def check_swatches(deck) -> int:
    """Swatch-differentiation check. Returns failure count (0 if the
    deck JSON is absent or has < 1 swatch)."""
    if deck is None:
        return 0
    swatches = [
        (sl.get("name", sl["hex"]), _rgb(sl["hex"]),
         ESPRESSO if sl.get("theme") == "dark" else ALABASTER)
        for sl in deck.get("slides", []) if sl.get("role") == "swatch"
    ]
    failures = 0
    for (na, ca, _), (nb, cb, _) in combinations(swatches, 2):
        d = _dist(ca, cb)
        if d < MIN_SWATCH_DIST:
            print(f"FAIL swatch-pair: {na} vs {nb} RGB dist {d:.1f} "
                  f"< {MIN_SWATCH_DIST} (indistinguishable at feed scale)")
            failures += 1
    for name, rgb, ground in swatches:
        d = _dist(rgb, ground)
        if d < MIN_SWATCH_DIST:
            print(f"FAIL swatch-ground: {name} RGB dist {d:.1f} from its "
                  f"slide ground < {MIN_SWATCH_DIST} (swatch invisible)")
            failures += 1
    if swatches and not failures:
        print(f"PASS swatch differentiation ({len(swatches)} swatches, "
              f"min pair dist >= {MIN_SWATCH_DIST})")
    return failures


def check_photos(deck_dir: Path, deck) -> int:
    """Photo-aware checks. Returns failure count (0 if no photo slides)."""
    if deck is None:
        return 0
    slides = deck.get("slides", [])
    photo_idx = [i for i, sl in enumerate(slides, 1) if sl.get("role") == "photo"]
    if not photo_idx:
        return 0
    meta_path = deck_dir / "_photo_meta.json"
    if not meta_path.exists():
        print(f"FAIL photo: {meta_path.name} missing -- re-render with the "
              f"current render_nuvarel.py")
        return 1
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    failures = 0
    for i in photo_idx:
        sl = slides[i - 1]
        m = meta.get(f"slide-{i}")
        if m is None:
            print(f"FAIL photo slide-{i}: no entry in _photo_meta.json")
            failures += 1
            continue
        key = sl.get("key")
        if key not in KEY_BANDS:
            print(f"FAIL photo slide-{i}: key must be one of "
                  f"{sorted(KEY_BANDS)} (got {key!r}) -- tonal rotation "
                  f"needs a declared key")
            failures += 1
        else:
            lo, hi = KEY_BANDS[key]
            lum = m["mean_luminance"]
            if not (lo <= lum < hi):
                print(f"FAIL photo slide-{i}: mean luminance {lum:.3f} outside "
                      f"'{key}' band [{lo}, {hi}) -- pick a different frame "
                      f"or declare the key the frame actually is")
                failures += 1
        if m["type_coverage"] > PHOTO_MAX_TYPE:
            print(f"FAIL photo slide-{i}: type covers {m['type_coverage']:.1%} "
                  f"of frame > {PHOTO_MAX_TYPE:.0%}")
            failures += 1
        if m["headline_words"] > PHOTO_MAX_WORDS:
            print(f"FAIL photo slide-{i}: {m['headline_words']} headline words "
                  f"> {PHOTO_MAX_WORDS}")
            failures += 1
        if m["silent"] and m["type_coverage"] > 0.0:
            print(f"FAIL photo slide-{i}: silent slide carries type "
                  f"({m['type_coverage']:.1%})")
            failures += 1
    if len(slides) >= 2:
        s2 = slides[1]
        if not (s2.get("role") == "photo" and s2.get("silent")):
            print("FAIL photo deck: slide 2 must be a silent photo slide "
                  "(strategy §8: frame 2 is a full-bleed photograph, no type)")
            failures += 1
    if not failures:
        keys = ",".join(str(slides[i - 1].get("key")) for i in photo_idx)
        print(f"PASS photo checks ({len(photo_idx)} photo slides, keys {keys}, "
              f"type <= {PHOTO_MAX_TYPE:.0%}, slide 2 silent)")
    return failures


def check(deck_dir: Path) -> int:
    pngs = sorted(
        deck_dir.glob("slide-*.png"),
        key=lambda p: int(p.stem.split("-")[1]),
    )
    if not pngs:
        print(f"FAIL: no slide PNGs in {deck_dir}")
        return 1
    deck = _load_deck(deck_dir)
    photo_slides = set()
    if deck is not None:
        photo_slides = {
            i for i, sl in enumerate(deck.get("slides", []), 1)
            if sl.get("role") == "photo"
        }
    prev_dir = deck_dir / "_preview350"
    prev_dir.mkdir(exist_ok=True)
    failures = 0
    for p in pngs:
        idx = int(p.stem.split("-")[1])
        img = Image.open(p).convert("RGB")
        ok_dim = img.size == (1080, 1350)
        img.resize((350, 438), Image.LANCZOS).save(prev_dir / p.name)
        if idx in photo_slides:
            status = "PASS" if ok_dim else "FAIL"
            if status == "FAIL":
                failures += 1
            print(f"{status} {p.name}: dim={img.size} (photo slide, ink band n/a)")
            continue
        small = img.resize((216, 270))  # cheap coverage estimate
        px = list(small.getdata())
        bg = Counter(px).most_common(1)[0][0]
        ink = sum(
            1 for c in px
            if max(abs(c[0] - bg[0]), abs(c[1] - bg[1]), abs(c[2] - bg[2])) > 40
        ) / len(px)
        ok_ink = BAND[0] <= ink <= BAND[1]
        status = "PASS" if (ok_dim and ok_ink) else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"{status} {p.name}: dim={img.size} ink={ink:.1%}")
    failures += check_swatches(deck)
    failures += check_photos(deck_dir, deck)
    print(f"previews -> {prev_dir}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(check(Path(sys.argv[1])))
