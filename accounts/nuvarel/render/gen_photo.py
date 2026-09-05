# -*- coding: utf-8 -*-
"""nuvarel photoreal still generator (Group CTO, 2026-09-05).

Productionises the 2026-09-05 photoreal spike
(render/out/photoreal-spike-2026-09-05/workflows/wan_t2i_brass_1088x1360_b3.json):
the local WAN 2.1 T2V 1.3B model already installed for video_lab is a
usable text-to-image generator at length=1. No new checkpoint, ₹0.

Talks to a locally running ComfyUI over its HTTP API (127.0.0.1:8188). It
does NOT start the server itself -- whether the GPU is free to take is a
judgment the calling agent makes (peers use the same GPU); if the server is
down it prints the exact start command and exits 2.

Usage:
    py -3 accounts/nuvarel/render/gen_photo.py --subject "<object, material, setting>" \
        --key dark|mid|light --out accounts/nuvarel/render/photos/<post-id> [--n 3] [--seed N]

Writes <out>/photo-<seed>-<i>.png (1088x1360, the renderer crops 4 px to
1080x1350) and <out>/gen-<seed>.json (prompts, workflow, timings). The
eyes-on pick is the caller's job: ~1/3 of frames carry a detached/off-frame
shadow or geometry artifact the numeric gate cannot see (spike finding 2),
so always generate >= 3 and look at every one before choosing.

Known limits carried from the spike (registry: instagram_accounts_social):
  - light key is UNPROVEN (every spike frame landed dark); the light prompt
    below is a first attempt, flagged "experimental" in gen-<seed>.json.
  - wood grain tends to render as flat laminate; a grain phrase is appended
    automatically when the subject names a wood, but check it on tap-to-open
    scale, not just at 350 px.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

COMFY_URL = "http://127.0.0.1:8188"
COMFY_DIR = (
    r"C:\Users\2026\Documents\income-engine\video_lab\samples\comfyui-mcp\ComfyUI"
)
START_CMD = (
    f'cd "{COMFY_DIR}" && ..\\.venv\\Scripts\\python.exe main.py --port 8188'
)

# Strategy §8 photography discipline, verbatim intent: one low warm light,
# desaturated, matte, real soft shadow, no people/hands/text.
BASE_POSITIVE = (
    "Editorial still-life photograph, {subject}. One single warm tungsten "
    "light source from the low left, about 3200K, casting one long soft "
    "shadow with gentle falloff{ground}. Muted desaturated colour grade, "
    "matte surfaces, no gloss, no reflections. Shallow depth of field, 85mm "
    "macro lens, fine film grain, quiet luxury interior magazine "
    "photography. Empty frame, only the object. No people, no hands, no text."
)
KEY_GROUND = {
    "dark": (
        " across a deep espresso-brown matte ground, low-key exposure, most "
        "of the frame in soft shadow"
    ),
    "mid": (
        " across a warm taupe linen surface, balanced mid-key exposure, "
        "neutral mid-tones dominant"
    ),
    "light": (
        " across a pale alabaster plaster surface, high-key exposure, bright "
        "airy and open, most of the frame light, the object small in a large "
        "pale field"
    ),
}
GRAIN_HINT = (
    " Deep open three-dimensional wood grain with visible pores, oiled solid "
    "timber, not laminate, not printed veneer."
)
WOOD_RE = re.compile(r"\b(wood|oak|walnut|teak|ash|maple|timber|mahogany)\b", re.I)

NEGATIVE = (
    "色调艳丽，过曝，细节模糊不清，字幕，风格，作品，画作，画面，整体发灰，最差质量，"
    "低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，"
    "畸形的，毁容的，形态畸形的肢体，手指融合，杂乱的背景, glossy, shiny, "
    "oversaturated, cartoon, illustration, anime, painting, 3d render, cgi, "
    "people, person, hand, face, text, watermark, logo, chrome, mirror"
)


def workflow(positive, negative, width, height, n, seed, steps, prefix):
    return {
        "37": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "wan2.1_t2v_1.3B_fp16.safetensors", "weight_dtype": "default"}},
        "38": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan",
            "device": "default"}},
        "39": {"class_type": "VAELoader", "inputs": {"vae_name": "wan_2.1_vae.safetensors"}},
        "40": {"class_type": "EmptyHunyuanLatentVideo", "inputs": {
            "width": width, "height": height, "length": 1, "batch_size": n}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["38", 0], "text": positive}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["38", 0], "text": negative}},
        "48": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["37", 0], "shift": 8}},
        "3": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": steps, "cfg": 6, "sampler_name": "uni_pc",
            "scheduler": "simple", "denoise": 1, "model": ["48", 0],
            "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["40", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["39", 0]}},
        "9": {"class_type": "SaveImage", "inputs": {
            "images": ["8", 0], "filename_prefix": prefix}},
    }


def server_up():
    try:
        with urllib.request.urlopen(f"{COMFY_URL}/system_stats", timeout=5) as r:
            return r.status == 200
    except (urllib.error.URLError, OSError):
        return False


def post_json(path, body):
    req = urllib.request.Request(
        f"{COMFY_URL}{path}", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def get_json(path):
    with urllib.request.urlopen(f"{COMFY_URL}{path}", timeout=30) as r:
        return json.loads(r.read())


def fetch_image(filename, subfolder, kind):
    q = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": kind})
    with urllib.request.urlopen(f"{COMFY_URL}/view?{q}", timeout=120) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--key", choices=list(KEY_GROUND), required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--width", type=int, default=1088)
    ap.add_argument("--height", type=int, default=1360)
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--timeout", type=int, default=900, help="seconds")
    args = ap.parse_args()

    if not server_up():
        print("FAIL: ComfyUI is not responding on 127.0.0.1:8188.")
        print("Start it (check nvidia-smi first -- peers share this GPU):")
        print(f"  {START_CMD}")
        print("then re-run. Stop it after the build if you started it.")
        return 2

    seed = args.seed if args.seed is not None else int(time.time()) % 2_000_000_000
    ground = KEY_GROUND[args.key]
    positive = BASE_POSITIVE.format(subject=args.subject.strip().rstrip("."), ground=ground)
    if WOOD_RE.search(args.subject):
        positive += GRAIN_HINT
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    prefix = f"nuvarel/{out.name}/photo-{seed}"
    wf = workflow(positive, NEGATIVE, args.width, args.height, args.n, seed, args.steps, prefix)

    t0 = time.time()
    pid = post_json("/prompt", {"prompt": wf})["prompt_id"]
    print(f"queued prompt_id={pid} seed={seed} key={args.key} n={args.n}", flush=True)
    entry = None
    while time.time() - t0 < args.timeout:
        time.sleep(4)
        try:
            hist = get_json(f"/history/{pid}")
        except (urllib.error.URLError, OSError) as e:
            print(f"poll error: {e}", flush=True)
            continue
        if pid in hist:
            st = hist[pid].get("status", {})
            if st.get("completed"):
                entry = hist[pid]
                break
            if st.get("status_str") == "error":
                print("FAIL: ComfyUI reported an execution error:")
                print(json.dumps(hist[pid], indent=1)[:3000])
                return 1
        print(f"  ...{time.time() - t0:.0f}s", flush=True)
    if entry is None:
        print(f"FAIL: timed out after {args.timeout}s (prompt_id {pid})")
        return 1

    saved = []
    for node_out in entry.get("outputs", {}).values():
        for i, im in enumerate(node_out.get("images", []), 1):
            data = fetch_image(im["filename"], im.get("subfolder", ""), im.get("type", "output"))
            dest = out / f"photo-{seed}-{i}.png"
            dest.write_bytes(data)
            saved.append(str(dest))
            print(f"  saved {dest}", flush=True)
    meta = {
        "seed": seed, "key": args.key, "experimental": args.key == "light",
        "subject": args.subject, "positive": positive, "negative": NEGATIVE,
        "width": args.width, "height": args.height, "n": args.n, "steps": args.steps,
        "wall_clock_s": round(time.time() - t0, 1), "prompt_id": pid, "files": saved,
    }
    (out / f"gen-{seed}.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK {len(saved)} image(s) in {meta['wall_clock_s']}s -> {out}")
    return 0 if saved else 1


if __name__ == "__main__":
    sys.exit(main())
