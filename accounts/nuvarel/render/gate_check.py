# -*- coding: utf-8 -*-
"""Nuvarel render gate: mechanical checks + feed-scale previews.

Checks per slide PNG in a rendered deck dir:
  1. exact 1080x1350 dimensions;
  2. ink coverage (fraction of pixels differing from the slide's modal
     background color by >40/255 in any channel) inside a 2-60% band:
     below = an empty/failed render, above = visual mud at feed scale.
     Swatch slides carry large color fields, hence the wide top of the
     band vs. text-only systems;
  3. writes 350px-wide previews to <dir>/_preview350/ .

Viewing the previews is still a mandatory human/agent step; the numbers
do not replace eyes (same doctrine as trend-signals-social's gate).

Usage: py -3 gate_check.py out/<slug>
"""
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

BAND = (0.02, 0.60)


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
    print(f"previews -> {prev_dir}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(check(Path(sys.argv[1])))
