# -*- coding: utf-8 -*-
"""Deterministic still-frame gate. Run BEFORE rendering a full sequence.

Why this exists (Group CTO, 2026-09-13). Six consecutive nuvarel cushion-press
previews reached the founder without any internal check, and round 6 was
rejected on two defects that are both measurable in a single still:

    blender_studio/output/cushion_press_test_still_f40.png
        p99-p1 luminance range .... 43     (washed out, no black point)
        stddev .................... 8.8    (flat grey field)
        mean saturation ........... 0.022

The thresholds below are CALIBRATED against the account's best-ever post
(2026-09-04-cables-read-cheap, 1,091 reach), measured over its 41 committed
QA frames, not guessed:

    p99-p1 luminance range .... median 203
    stddev .................... median 51.1
    mean saturation ........... median 0.081   <- note

That last number matters. A saturation floor of 0.15 was proposed in the
round-6 diagnosis; it would have FAILED the account's best post. nuvarel is a
deliberately desaturated brand (`docs/nuvarel-strategy.md` section 8:
"Saturation is the loudest cheap signal there is"), so saturation is gated
from BOTH sides: a floor that catches a washed-out render, and a ceiling that
catches a render that has gone loud.

Solid title/end cards (the espresso end card in every nuvarel Reel) legitimately
have near-zero range. They are auto-detected and skipped rather than waived by
hand, so the gate cannot be argued past.

Usage:
    py -3 scripts/frame_gate.py <png|dir> [--profile nuvarel] [--json]

Exit code 0 = PASS, 1 = FAIL. Wire it into a build before `render_reel.py`,
not after.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import sys
from pathlib import Path

from PIL import Image, ImageStat

# Calibrated on 2026-09-04-cables-read-cheap QA frames (n=41, end card excluded).
PROFILES = {
    "nuvarel": {
        "range_min": 150,      # winning median 203; round-6 reject 43
        "stddev_min": 30.0,    # winning median 51.1; round-6 reject 8.8
        "dark_frac_min": 0.010,  # a real black point must exist somewhere
        "sat_min": 0.040,      # winning min 0.051; round-6 reject 0.022
        "sat_max": 0.350,      # brand rule: desaturated grade
    },
    # Meme/high-energy accounts run louder. Floors only, no ceiling.
    "loud": {
        "range_min": 150,
        "stddev_min": 30.0,
        "dark_frac_min": 0.010,
        "sat_min": 0.040,
        "sat_max": 1.0,
    },
}


def is_solid_card(hist: list[int], total: int) -> bool:
    """True when >=90% of pixels sit within +/-12 levels of the modal bin.

    Catches a deliberate flat title/end card so it is not judged on contrast.
    """
    mode = max(range(256), key=lambda i: hist[i])
    lo, hi = max(0, mode - 12), min(255, mode + 12)
    return sum(hist[lo:hi + 1]) >= total * 0.90


def measure(path: Path) -> dict:
    im = Image.open(path).convert("RGB")
    grey = im.convert("L")
    hist = grey.histogram()
    total = sum(hist)

    def pct(p: float) -> int:
        run = 0
        for i, v in enumerate(hist):
            run += v
            if run >= total * p:
                return i
        return 255

    small = im.resize((108, 192))
    px = list(small.getdata())
    sat = sum(colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1] for r, g, b in px) / len(px)

    return {
        "frame": path.name,
        "range": pct(0.99) - pct(0.01),
        "stddev": round(ImageStat.Stat(grey).stddev[0], 2),
        "dark_frac": round(sum(hist[:60]) / total, 4),
        "sat": round(sat, 4),
        "solid_card": is_solid_card(hist, total),
    }


def judge(m: dict, t: dict) -> list[str]:
    if m["solid_card"]:
        return []
    fails = []
    if m["range"] < t["range_min"]:
        fails.append(f"dynamic range {m['range']} < {t['range_min']} (washed out / no black point)")
    if m["stddev"] < t["stddev_min"]:
        fails.append(f"contrast stddev {m['stddev']} < {t['stddev_min']} (flat field)")
    if m["dark_frac"] < t["dark_frac_min"]:
        fails.append(f"dark pixels {m['dark_frac']} < {t['dark_frac_min']} (nothing anchors the low end)")
    if m["sat"] < t["sat_min"]:
        fails.append(f"saturation {m['sat']} < {t['sat_min']} (colour has drained out)")
    if m["sat"] > t["sat_max"]:
        fails.append(f"saturation {m['sat']} > {t['sat_max']} (louder than the brand grade)")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="a PNG, or a directory of PNGs")
    ap.add_argument("--profile", default="nuvarel", choices=sorted(PROFILES))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    p = Path(a.target)
    frames = sorted(p.glob("*.png")) if p.is_dir() else [p]
    if not frames:
        print(f"FATAL: no PNG frames under {p}", file=sys.stderr)
        return 1

    t = PROFILES[a.profile]
    results, failed = [], 0
    for f in frames:
        m = measure(f)
        m["fails"] = judge(m, t)
        if m["fails"]:
            failed += 1
        results.append(m)

    if a.json:
        print(json.dumps({"profile": a.profile, "thresholds": t, "frames": results}, indent=2))
    else:
        print(f"frame gate [{a.profile}]  {len(frames)} frame(s)")
        print(f"{'frame':<26}{'range':>7}{'stddev':>8}{'dark':>8}{'sat':>8}  verdict")
        for m in results:
            tag = "CARD" if m["solid_card"] else ("FAIL" if m["fails"] else "pass")
            print(f"{m['frame']:<26}{m['range']:>7}{m['stddev']:>8}{m['dark_frac']:>8}{m['sat']:>8}  {tag}")
            for x in m["fails"]:
                print(f"    - {x}")
    print(f"\n{'FAIL' if failed else 'PASS'}: {failed}/{len(frames)} frame(s) below the bar")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
