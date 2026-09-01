# -*- coding: utf-8 -*-
"""Nuvarel render gate: mechanical checks + feed-scale previews.

Checks per slide PNG in a rendered deck dir:
  1. exact 1080x1350 dimensions;
  2. ink coverage (fraction of pixels differing from the slide's modal
     background color by >40/255 in any channel) inside a 2-60% band:
     below = an empty/failed render, above = visual mud at feed scale.
     Swatch slides carry large color fields, hence the wide top of the
     band vs. text-only systems;
  3. writes 350px-wide previews to <dir>/_preview350/ ;
  4. swatch differentiation (added 2026-09-01 after a CCO-caught defect:
     two near-identical swatches and one swatch invisible on its own
     ground shipped to review): if ../decks/<slug>.json exists, every
     pair of swatch hexes must be >= MIN_SWATCH_DIST apart (Euclidean
     RGB), and each swatch must be >= MIN_SWATCH_DIST from its own
     slide ground (espresso if the slide is theme "dark", alabaster
     otherwise). Ink-vs-background alone cannot see this class.

Viewing the previews is still a mandatory human/agent step; the numbers
do not replace eyes (same doctrine as trend-signals-social's gate).

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


def _rgb(hexcode):
    h = hexcode.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def check_swatches(deck_dir: Path) -> int:
    """Swatch-differentiation check. Returns failure count (0 if the
    deck JSON is absent or has < 1 swatch)."""
    deck_path = deck_dir.parent.parent / "decks" / f"{deck_dir.name}.json"
    if not deck_path.exists():
        return 0
    deck = json.loads(deck_path.read_text(encoding="utf-8"))
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


def check(deck_dir: Path) -> int:
    pngs = sorted(
        deck_dir.glob("slide-*.png"),
        key=lambda p: int(p.stem.split("-")[1]),
    )
    if not pngs:
        print(f"FAIL: no slide PNGs in {deck_dir}")
        return 1
    prev_dir = deck_dir / "_preview350"
    prev_dir.mkdir(exist_ok=True)
    failures = 0
    for p in pngs:
        img = Image.open(p).convert("RGB")
        ok_dim = img.size == (1080, 1350)
        small = img.resize((216, 270))  # cheap coverage estimate
        px = list(small.getdata())
        bg = Counter(px).most_common(1)[0][0]
        ink = sum(
            1 for c in px
            if max(abs(c[0] - bg[0]), abs(c[1] - bg[1]), abs(c[2] - bg[2])) > 40
        ) / len(px)
        ok_ink = BAND[0] <= ink <= BAND[1]
        img.resize((350, 438), Image.LANCZOS).save(prev_dir / p.name)
        status = "PASS" if (ok_dim and ok_ink) else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"{status} {p.name}: dim={img.size} ink={ink:.1%}")
    failures += check_swatches(deck_dir)
    print(f"previews -> {prev_dir}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(check(Path(sys.argv[1])))
