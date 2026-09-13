"use strict";
/* curator.js -- nuvarel's own stickman, REWRITTEN 2026-09-13.

   The founder rejected the "Curator Mk II" redesign in
   docs/visual/nuvarel-curator-mk2.md outright: "the earlier stickman was
   better than this, it just needed some refinement." This file throws
   away Mk II's 8.5-head proportions, faceless ovoid head and three-shape
   hand system, and goes back to the ORIGINAL assets/rig2d.js skeleton --
   same numbers, not eyeballed-and-drifted:
     torso 170, neck 26, head r56, upper arm 95, lower arm 88,
     upper leg 105, lower leg 105 (4.58 heads tall).

   Only four targeted changes on top of that original skeleton:
     1. Face kept -- dot eyes, same logic as rig2d.js's poseStick. Mk II's
        facelessness is walked back, not "refined further."
     2. A light amount of limb taper: each limb is two polylines (upper
        segment thicker, lower thinner) instead of one uniform stroke --
        small, not a bezier-ribbon redesign.
     3. Small rounded hand/foot circles at each limb's line-end instead
        of a bare stroke cap -- a simple filled dot, not Mk II's
        flat/pinch/grip wedge system.
     4. Nuvarel's own taupe/bronze palette (docs/nuvarel-strategy.md §8:
        alabaster #F2EEE6, espresso #2A241E, taupe #6E6257, bronze
        #9C7A4F) instead of the generic near-black/cream every other
        account's shared stickman uses, plus one small bronze belt
        accent (<=2% of frame) -- so the figure reads as nuvarel's own
        without changing the silhouette the founder already liked.

   Kept as its own account-local file (not merged into the shared
   assets/rig2d.js) for the same reason as before: this is nuvarel's own
   character, not the shared meme rig -- even though the skeleton math is
   now intentionally identical to it. Full history, including the
   rejected Mk II spec, is in docs/visual/nuvarel-curator-mk2.md.

   Depends on rig2d.js being loaded first on the page for its generic
   math/DOM helpers (el, dir, D2R, clamp, lerp, ramp, easing fns) and its
   pose vocabulary (P, mixPose, walkPose) -- a curator Reel can reuse the
   exact same pose dicts a hype_tingles Reel does (P.stand, P.carry,
   etc.), just driven through makeCurator/poseCurator instead of
   makeStick/poseStick. */

const CURATOR_COLORS = {
  taupe: "#6E6257",
  taupeDark: "#B8AFA2",
  alabaster: "#F2EEE6",
  espresso: "#2A241E",
  bronze: "#9C7A4F"
};

/* identical to rig2d.js's internal L -- restated here so this file has
   no silent runtime dependency on rig2d.js's private constant, only on
   its exported helpers. Do not drift these numbers; they ARE the
   proportion the founder recognized and approved. */
const CURATOR_L = { torso: 170, neck: 26, head: 56, uArm: 95, lArm: 88, uLeg: 105, lLeg: 105 };

function makeCurator(parent, opts) {
  const o = opts || {};
  const stroke = o.stroke || CURATOR_COLORS.taupe;
  const headFill = o.headFill || CURATOR_COLORS.alabaster;
  const eyeColor = o.eyeColor || CURATOR_COLORS.espresso;
  const wU = o.wUpper || 17, wL = o.wLower || 12, hw = o.hw || 14, ew = o.ew || 9;
  const g = el(parent, "g", {});
  const capU = { stroke, "stroke-width": wU, "stroke-linecap": "round", fill: "none", "stroke-linejoin": "round" };
  const capL = { stroke, "stroke-width": wL, "stroke-linecap": "round", fill: "none", "stroke-linejoin": "round" };
  const limb = () => ({
    upper: el(g, "polyline", capU),
    lower: el(g, "polyline", capL),
    end: el(g, "circle", { r: (wL / 2) + 3, fill: stroke })
  });
  const c = {
    g, stroke, headFill, eyeColor,
    torso: el(g, "polyline", capU),
    /* clavicle: only drawn when a pose sets shoulderW (see poseCurator) */
    clav: el(g, "line", { stroke, "stroke-width": wU, "stroke-linecap": "round", display: "none" }),
    lArm: limb(), rArm: limb(), lLeg: limb(), rLeg: limb(),
    /* one small bronze accent -- a belt line at the waist, never on a
       limb -- the one nuvarel-specific color touch beyond the taupe body. */
    /* opts.belt === false hides it. Needed when a shot puts the hip right at a
       prop's surface line: the accent then reads as a stray bronze mark on the
       prop rather than as clothing (measured, press-test preview 4, 2026-09-13). */
    belt: el(g, "line", { stroke: CURATOR_COLORS.bronze, "stroke-width": 6, "stroke-linecap": "round",
                          display: o.belt === false ? "none" : "" }),
    head: el(g, "circle", { fill: headFill, stroke, "stroke-width": hw }),
    eyeL: el(g, "ellipse", { fill: eyeColor }), eyeR: el(g, "ellipse", { fill: eyeColor }),
    lidL: el(g, "line", { stroke, "stroke-width": ew, "stroke-linecap": "round" }),
    lidR: el(g, "line", { stroke, "stroke-width": ew, "stroke-linecap": "round" })
  };
  return c;
}

/* poseCurator: same pose dict shape as rig2d.js's poseStick (tx,ty,rot,
   torso,headTilt,laU/laL/raU/raL,llU/llL/rlU/rlL,eyes,face,sx,sy,px,py)
   -- any existing P.* pose or mixPose/walkPose result works unmodified.

   ONE optional extra field, added 2026-09-13: `shoulderW` (default 0, so
   every existing pose renders exactly as it did before). When set, the two
   arms originate at +/- shoulderW perpendicular to the torso instead of both
   starting at the single neck point, and a short clavicle is drawn between
   them. The shared rig has no shoulder width because it was built for SIDE
   views, where one shoulder hides the other. Head-on, two arms leaving one
   point read as a tripod rather than a person -- measured on the first
   press-test preview, 2026-09-13. Leave it at 0 for any profile shot; set it
   to about 24 for a front-facing two-hand action.
   `p.laPivot` / `p.raPivot` (world-space, optional) are written back by this
   function so a caller doing IK knows where each arm actually starts. */
function poseCurator(s, p) {
  const hip = [0, 0];
  const tTop = [hip[0] + dir(p.torso)[0] * CURATOR_L.torso, hip[1] + dir(p.torso)[1] * CURATOR_L.torso];
  const headC = [tTop[0] + dir(p.torso + (p.headTilt || 0))[0] * (CURATOR_L.neck + CURATOR_L.head * 0.9),
                 tTop[1] + dir(p.torso + (p.headTilt || 0))[1] * (CURATOR_L.neck + CURATOR_L.head * 0.9)];
  const seg = (o, a1, l1, a2, l2) => {
    const m = [o[0] + dir(a1)[0] * l1, o[1] + dir(a1)[1] * l1];
    const e = [m[0] + dir(a2)[0] * l2, m[1] + dir(a2)[1] * l2];
    return [o, m, e];
  };
  const pts = a => a.map(q => q[0].toFixed(1) + "," + q[1].toFixed(1)).join(" ");
  const setLimb = (limb, o, a1, l1, a2, l2) => {
    const [oo, m, e] = seg(o, a1, l1, a2, l2);
    limb.upper.setAttribute("points", pts([oo, m]));
    limb.lower.setAttribute("points", pts([m, e]));
    limb.end.setAttribute("cx", e[0].toFixed(1));
    limb.end.setAttribute("cy", e[1].toFixed(1));
  };

  /* shoulder pivots: both at the neck point unless shoulderW is set */
  const sw = p.shoulderW || 0;
  const sperp = dir(p.torso + 90);
  const lSh = [tTop[0] - sperp[0] * sw, tTop[1] - sperp[1] * sw];
  const rSh = [tTop[0] + sperp[0] * sw, tTop[1] + sperp[1] * sw];
  if (sw > 0) {
    s.clav.setAttribute("display", "");
    s.clav.setAttribute("x1", lSh[0].toFixed(1)); s.clav.setAttribute("y1", lSh[1].toFixed(1));
    s.clav.setAttribute("x2", rSh[0].toFixed(1)); s.clav.setAttribute("y2", rSh[1].toFixed(1));
  } else {
    s.clav.setAttribute("display", "none");
  }

  s.torso.setAttribute("points", pts([hip, tTop]));
  setLimb(s.lArm, lSh, p.laU, CURATOR_L.uArm, p.laL, CURATOR_L.lArm);
  setLimb(s.rArm, rSh, p.raU, CURATOR_L.uArm, p.raL, CURATOR_L.lArm);
  setLimb(s.lLeg, hip, p.llU, CURATOR_L.uLeg, p.llL, CURATOR_L.lLeg);
  setLimb(s.rLeg, hip, p.rlU, CURATOR_L.uLeg, p.rlL, CURATOR_L.lLeg);
  p.laPivot = lSh; p.raPivot = rSh;

  const beltHalf = 13;
  const perp = dir(p.torso + 90);
  s.belt.setAttribute("x1", (hip[0] + perp[0] * beltHalf).toFixed(1));
  s.belt.setAttribute("y1", (hip[1] + perp[1] * beltHalf).toFixed(1));
  s.belt.setAttribute("x2", (hip[0] - perp[0] * beltHalf).toFixed(1));
  s.belt.setAttribute("y2", (hip[1] - perp[1] * beltHalf).toFixed(1));

  s.head.setAttribute("cx", headC[0]); s.head.setAttribute("cy", headC[1]); s.head.setAttribute("r", CURATOR_L.head);

  /* face: same eyes/lids logic as rig2d.js's poseStick, unchanged. */
  const f = p.face === undefined ? 1 : p.face, ex = headC[0] + f * 16, ey = headC[1] - 6, gap = 21;
  const eyes = p.eyes || "open";
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
