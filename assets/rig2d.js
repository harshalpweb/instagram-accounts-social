"use strict";
/* rig2d.js -- shared 2D stickman rig + animation-principle helpers.
   Extracted verbatim from the approved hype_tingles H1 prototype
   (income-engine/blender_studio/scenes/reels_2d/hype_h1_morning_routine_2d/),
   parameterized for per-account palettes. Every reel.html owns its own
   beat table, scenery and seek(); this file owns the rig and the physics
   vocabulary (anticipation windups, squash & stretch, punch/shake,
   snap-in overlays, the Chromium stale-paint guard). */

const TAU = Math.PI * 2;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, k) => a + (b - a) * k;
const ramp = (t, a, b) => clamp((t - a) / (b - a), 0, 1);
const easeOutCubic = k => 1 - Math.pow(1 - k, 3);
const easeInCubic = k => k * k * k;
const easeInOutQuad = k => k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
const easeInOutCubic = k => k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
const easeOutBack = k => { const c = 1.70158; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const easeOutBackBig = k => { const c = 3.2; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
/* impulse that starts at max at t0 and decays -- zoom punches */
const punch = (t, t0, amp, decay) => t < t0 ? 0 : amp * Math.exp(-(t - t0) * decay);
/* decaying oscillation -- camera shake */
const shake = (t, t0, amp, decay, freq, ph) => t < t0 ? 0 : amp * Math.exp(-(t - t0) * decay) * Math.sin((t - t0) * freq * TAU + ph);
const D2R = Math.PI / 180;
const dir = a => [Math.sin(a * D2R), Math.cos(a * D2R)]; /* 0=down 90=screen-right 180=up */

const SVGNS = "http://www.w3.org/2000/svg";
function el(parent, tag, attrs) { const e = document.createElementNS(SVGNS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; }

/* ---------------- stickman rig (FK, pose = angle set) ----------------
   Pose fields (angles deg, 0=down 90=screen-right 180=up):
   tx,ty hip position; rot whole-body (optional pivot rx,ry); torso angle;
   headTilt extra; laU,laL,raU,raL arm segs; llU,llL,rlU,rlL leg segs;
   eyes open|wide|dead|closed; face -1..1; sx,sy squash about px,py. */
const L = { torso: 170, neck: 26, head: 56, uArm: 95, lArm: 88, uLeg: 105, lLeg: 105 };

function makeStick(parent, opts) {
  const o = opts || {};
  const stroke = o.stroke || "#F4F2EC", fill = o.fill || "#111015";
  const w = o.w || 17, hw = o.hw || 15, ew = o.ew || 9;
  const g = el(parent, "g", {});
  const cap = { "stroke": stroke, "stroke-width": w, "stroke-linecap": "round", "fill": "none", "stroke-linejoin": "round" };
  const mk = () => el(g, "polyline", cap);
  const s = {
    g, stroke, fill,
    lArm: mk(), lLeg: mk(), torso: mk(), rLeg: mk(), rArm: mk(),
    head: el(g, "circle", { "fill": fill, "stroke": stroke, "stroke-width": hw }),
    tuft: o.tuft ? el(g, "path", { "stroke": o.tuft, "stroke-width": 11, "fill": "none", "stroke-linecap": "round" }) : null,
    eyeL: el(g, "ellipse", { fill: stroke }), eyeR: el(g, "ellipse", { fill: stroke }),
    lidL: el(g, "line", { "stroke": stroke, "stroke-width": ew, "stroke-linecap": "round" }),
    lidR: el(g, "line", { "stroke": stroke, "stroke-width": ew, "stroke-linecap": "round" })
  };
  return s;
}

function poseStick(s, p) {
  const hip = [0, 0];
  const tTop = [hip[0] + dir(p.torso)[0] * L.torso, hip[1] + dir(p.torso)[1] * L.torso];
  const headC = [tTop[0] + dir(p.torso + (p.headTilt || 0))[0] * (L.neck + L.head * 0.9),
                 tTop[1] + dir(p.torso + (p.headTilt || 0))[1] * (L.neck + L.head * 0.9)];
  const seg = (o, a1, l1, a2, l2) => { const m = [o[0] + dir(a1)[0] * l1, o[1] + dir(a1)[1] * l1];
    return [o, m, [m[0] + dir(a2)[0] * l2, m[1] + dir(a2)[1] * l2]]; };
  const pts = a => a.map(q => q[0].toFixed(1) + "," + q[1].toFixed(1)).join(" ");
  s.torso.setAttribute("points", pts([hip, tTop]));
  s.lArm.setAttribute("points", pts(seg(tTop, p.laU, L.uArm, p.laL, L.lArm)));
  s.rArm.setAttribute("points", pts(seg(tTop, p.raU, L.uArm, p.raL, L.lArm)));
  s.lLeg.setAttribute("points", pts(seg(hip, p.llU, L.uLeg, p.llL, L.lLeg)));
  s.rLeg.setAttribute("points", pts(seg(hip, p.rlU, L.uLeg, p.rlL, L.lLeg)));
  s.head.setAttribute("cx", headC[0]); s.head.setAttribute("cy", headC[1]); s.head.setAttribute("r", L.head);
  if (s.tuft) { /* small hair-flick on top of the head, follows facing dir */
    const f0 = p.face === undefined ? 1 : (p.face >= 0 ? 1 : -1);
    s.tuft.setAttribute("d", `M ${headC[0] - 8 * f0} ${headC[1] - L.head - 4} q ${18 * f0} -26 ${44 * f0} -18`);
  }
  /* face: eyes offset toward facing dir */
  const f = p.face === undefined ? 1 : p.face, ex = headC[0] + f * 16, ey = headC[1] - 6, gap = 21;
  const eyes = p.eyes || "open";
  /* NB: display, NOT visibility -- an explicit visibility:visible on a child
     resurrects it inside a visibility:hidden ancestor (this exact bug shipped
     ghost eyelids/z-glyphs from hidden shots into 3 probe rounds). */
  const show = (e, on) => e.setAttribute("display", on ? "" : "none");
  const setE = (e, x, rx, ry) => { e.setAttribute("cx", x); e.setAttribute("cy", ey); e.setAttribute("rx", rx); e.setAttribute("ry", ry); };
  if (eyes === "open") { show(s.eyeL, 1); show(s.eyeR, 1); show(s.lidL, 0); show(s.lidR, 0); setE(s.eyeL, ex - gap, 7, 9); setE(s.eyeR, ex + gap, 7, 9); }
  else if (eyes === "wide") { show(s.eyeL, 1); show(s.eyeR, 1); show(s.lidL, 0); show(s.lidR, 0); setE(s.eyeL, ex - gap, 12, 14); setE(s.eyeR, ex + gap, 12, 14); }
  else if (eyes === "dead") { show(s.eyeL, 0); show(s.eyeR, 0); show(s.lidL, 1); show(s.lidR, 1);
    s.lidL.setAttribute("x1", ex - gap - 11); s.lidL.setAttribute("x2", ex - gap + 11); s.lidL.setAttribute("y1", ey); s.lidL.setAttribute("y2", ey);
    s.lidR.setAttribute("x1", ex + gap - 11); s.lidR.setAttribute("x2", ex + gap + 11); s.lidR.setAttribute("y1", ey); s.lidR.setAttribute("y2", ey); }
  else { /* closed */
    show(s.eyeL, 0); show(s.eyeR, 0); show(s.lidL, 1); show(s.lidR, 1);
    s.lidL.setAttribute("x1", ex - gap - 10); s.lidL.setAttribute("x2", ex - gap + 10); s.lidL.setAttribute("y1", ey + 3); s.lidL.setAttribute("y2", ey + 3);
    s.lidR.setAttribute("x1", ex + gap - 10); s.lidR.setAttribute("x2", ex + gap + 10); s.lidR.setAttribute("y1", ey + 3); s.lidR.setAttribute("y2", ey + 3); }
  const sx = p.sx || 1, sy = p.sy || 1, px = p.px || 0, py = p.py || 0;
  const rot = (p.rx || p.ry) ? `rotate(${p.rot || 0},${p.rx || 0},${p.ry || 0})` : `rotate(${p.rot || 0})`;
  s.g.setAttribute("transform",
    `translate(${p.tx},${p.ty}) ${rot} translate(${px},${py}) scale(${sx},${sy}) translate(${-px},${-py})`);
}

const mixPose = (a, b, k) => { const o = {}; for (const key in a) { o[key] = (typeof a[key] === "number" && typeof b[key] === "number") ? lerp(a[key], b[key], k) : (k < 0.5 ? a[key] : b[key]); } for (const key in b) if (!(key in o)) o[key] = b[key]; return o; };

/* base pose vocabulary (hip-local angle sets) -- reels extend/override */
const P = {
  idle:   { rot: 0, torso: 180, laU: 12, laL: 6, raU: -12, raL: -6, llU: 6, llL: 2, rlU: -6, rlL: -2, eyes: "open", face: 1 },
  stand:  { rot: 0, torso: 180, laU: 14, laL: 8, raU: -14, raL: -8, llU: 6, llL: 2, rlU: -6, rlL: -2, eyes: "open", face: 1 },
  sleep:  { rot: -90, torso: 180, headTilt: 0, laU: 55, laL: 135, raU: 40, raL: 120, llU: 10, llL: -4, rlU: -6, rlL: 4, eyes: "closed", face: -0.2 },
  curl:   { rot: -90, torso: 170, laU: 40, laL: 100, raU: 25, raL: 85, llU: 60, llL: -30, rlU: 45, rlL: -15, eyes: "closed", face: -0.2 },
  launch: { rot: 0, torso: 182, laU: 225, laL: 250, raU: 135, raL: 110, llU: 30, llL: 80, rlU: -18, rlL: -60, eyes: "wide", face: 1 },
  apex:   { rot: 0, torso: 180, laU: 120, laL: 100, raU: -120, raL: -100, llU: 35, llL: -30, rlU: -35, rlL: 30, eyes: "wide", face: 1 },
  landCrouch: { rot: 0, torso: 176, laU: 115, laL: 70, raU: -115, raL: -70, llU: 48, llL: -8, rlU: -48, rlL: 8, eyes: "wide", face: 1 },
  windup: { rot: 8, torso: 150, laU: -70, laL: -75, raU: -55, raL: -60, llU: 55, llL: -15, rlU: -40, rlL: 12, eyes: "open", face: 1 },
  ball:   { rot: 20, torso: 160, laU: 95, laL: -165, raU: 85, raL: -155, llU: 100, llL: -140, rlU: 88, rlL: -130, eyes: "closed", face: 1 },
  zen:    { rot: 0, torso: 180, laU: 55, laL: -25, raU: -55, raL: 25, llU: 80, llL: -155, rlU: -80, rlL: 155, eyes: "closed", face: 0 },
  sprint: { rot: 0, torso: 158, laU: 110, laL: 60, raU: -60, raL: -120, llU: 70, llL: 15, rlU: -55, rlL: -25, eyes: "wide", face: -1 },
  dive:   { rot: -90, torso: 180, laU: 186, laL: 178, raU: 174, raL: 182, llU: 12, llL: -8, rlU: -10, rlL: 6, eyes: "wide", face: -1 },
  flat:   { rot: -90, torso: 180, laU: 60, laL: 140, raU: 45, raL: 125, llU: 8, llL: -3, rlU: -6, rlL: 3, eyes: "closed", face: -0.2 },
  /* seated, side view facing screen-right: hips on a seat, knees bent forward */
  sitUp:  { rot: 0, torso: 172, laU: 60, laL: 95, raU: 50, raL: 100, llU: 78, llL: 8, rlU: 70, rlL: 4, eyes: "open", face: 1 },
  sitSlouch: { rot: 0, torso: 140, headTilt: -25, laU: 55, laL: 60, raU: 45, raL: 55, llU: 85, llL: 15, rlU: 78, rlL: 10, eyes: "open", face: 1 },
  sitFlop: { rot: 0, torso: 112, headTilt: -35, laU: 40, laL: 30, raU: 30, raL: 25, llU: 95, llL: 30, rlU: 88, rlL: 24, eyes: "dead", face: 1 },
  /* formal walk (briefcase arm stays down) */
  walkA:  { rot: 0, torso: 178, laU: 35, laL: 20, raU: -25, raL: -10, llU: 30, llL: 8, rlU: -28, rlL: -20, eyes: "open", face: 1 },
  walkB:  { rot: 0, torso: 178, laU: -25, laL: -12, raU: 30, raL: 18, llU: -26, llL: -18, rlU: 32, rlL: 10, eyes: "open", face: 1 },
  /* reach up (facing right, both arms raised toward a point up-right) */
  reachUp: { rot: 0, torso: 184, laU: 168, laL: 150, raU: 152, raL: 138, llU: 8, llL: 2, rlU: -8, rlL: -2, eyes: "open", face: 1 },
  /* two-hand carry in front (object rides with hands) */
  carry:  { rot: 0, torso: 176, laU: 105, laL: 55, raU: 95, raL: 48, llU: 6, llL: 2, rlU: -6, rlL: -2, eyes: "open", face: 1 },
  kneel:  { rot: 0, torso: 150, headTilt: -20, laU: 120, laL: 85, raU: 105, raL: 70, llU: 60, llL: -95, rlU: 45, rlL: -110, eyes: "open", face: 1 },
};

/* walk-cycle mixer: phase 0..1 across one stride (A -> B -> A) */
function walkPose(ph, base) {
  const a = base ? base.a : P.walkA, b = base ? base.b : P.walkB;
  const k = ph < 0.5 ? easeInOutQuad(ph / 0.5) : easeInOutQuad(1 - (ph - 0.5) / 0.5);
  const p = mixPose({ ...a }, { ...b }, k);
  p.ty = (p.ty || 0); /* caller sets tx/ty; bob added by caller via Math.abs(sin) */
  return p;
}

/* ---------------- overlay snap helpers ---------------- */
function snapIn(e, t, t0, dur = 0.14, tilt = 0) {
  if (t < t0) { e.style.visibility = "hidden"; return; }
  e.style.visibility = "visible";
  const k = ramp(t, t0, t0 + dur), s = lerp(2.1, 1, easeOutBackBig(k));
  e.style.transform = `scale(${s.toFixed(3)}) rotate(${tilt}deg)`;
}
function textIn(e, t, t0, dur = 0.12) {
  if (t < t0) { e.style.visibility = "hidden"; return; }
  e.style.visibility = "visible";
  const k = ramp(t, t0, t0 + dur), s = lerp(1.35, 1, easeOutBack(k));
  e.style.transform = `scale(${s.toFixed(3)})`;
}
/* calm variant for nuvarel: fade + 20px rise, no overshoot */
function fadeUp(e, t, t0, dur = 0.5) {
  if (t < t0) { e.style.visibility = "hidden"; e.style.opacity = 0; return; }
  e.style.visibility = "visible";
  const k = easeInOutCubic(ramp(t, t0, t0 + dur));
  e.style.opacity = k.toFixed(3);
  e.style.transform = `translateY(${(20 * (1 - k)).toFixed(1)}px)`;
}
/* floating z glyphs above a sleeper */
function zs(arr, t, x, y, on) {
  arr.forEach((z, i) => {
    if (!on) { z.setAttribute("display", "none"); return; }
    const ph = ((t * 0.55 + i * 0.33) % 1);
    z.setAttribute("display", "");
    z.setAttribute("x", x + i * 8 + Math.sin((t + i) * 2) * 10 + ph * 30);
    z.setAttribute("y", y - ph * 130);
    z.setAttribute("opacity", (1 - ph).toFixed(2));
    z.setAttribute("font-size", 30 + ph * 26);
  });
}

/* ---------------- Chromium stale-paint guard ----------------
   Verified across 3 probe rounds on this box: ghost sprites survive DOM
   re-append, display-toggle AND a body-bg flip (body bg is a composited
   solid-color quad; it never damages the #cam/#ui layers' cached tiles).
   Flip 1 LSB INSIDE each layer instead: full-canvas rect at the bottom of
   the svg + near-transparent bg on #ui -- visually imperceptible, but it
   damages the full layer so every tile re-rasters. Call from seek(). */
function makeFlipRect(stage) { return el(stage, "rect", { x: 0, y: 0, width: 1080, height: 1920, fill: "none" }); }
function stalePaintGuard(t, flipRect, uiEl, rgba) {
  const odd = Math.round(t * 30) % 2;
  flipRect.setAttribute("fill", odd ? (rgba || "rgba(17,16,21,0.004)") : "none");
  uiEl.style.backgroundColor = odd ? (rgba || "rgba(17,16,21,0.004)") : "transparent";
}
/* seek() must resolve only after a real compositor commit (double rAF);
   render_reel.py's page.evaluate awaits the returned promise. */
const compositorCommit = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
