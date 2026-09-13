"use strict";
/* curator.js -- nuvarel-only "Curator Mk II" character rig.

   Dedicated to this account. Do NOT merge this into the shared
   assets/rig2d.js -- the original Curator's failure was exactly that: a
   rig reused across accounts (hype_tingles' meme stickman, including a
   sitFlop/eyes:"dead" pose) standing in for a bespoke wealth-signalling
   figure. Full design brief: docs/visual/nuvarel-curator-mk2.md.

   Depends on rig2d.js's generic math/DOM helpers being loaded first in
   the page (el(), clamp, lerp, ramp, easeInOutCubic, stalePaintGuard,
   compositorCommit) -- those are generic rendering-pipeline utilities,
   not "the character", so sharing them is fine; only the character
   geometry/pose vocabulary lives here.

   Ported from the preview-only static reference-sheet generator
   (session scratchpad gen_curator_mk2.py, not part of this repo) that
   produced curator_mk2_sheet.png -- same geometry, same pose numbers,
   now driven per-frame instead of baked into a static SVG.

   IMPORTANT: pose parameters (el_dx/el_dy/wr_dx/wr_dy etc.) are
   hand-authored control points on a quadratic-bezier "ribbon" per limb,
   NOT a rigid forward-kinematics skeleton -- the declared bone lengths
   in CURATOR_L are for scale reference only. Author new poses by
   nudging numbers and looking at rendered frames, not by solving IK. */

const CURATOR_COLORS = {
  taupe: "#6E6257",       // figure body, mid-key scenes
  taupeDark: "#B8AFA2",   // figure body, dark-key variant
  garmentLight: "#E4DCCB",
  garmentDark: "#4A4138",
  bronze: "#9C7A4F"
};

const CURATOR_L = {
  headRx: 26, headRy: 33, neckLen: 30, torso: 175,
  uArm: 112, lArm: 100, hand: 20,
  uLeg: 142, lLeg: 136, foot: 14,
  totalHeight: 563,
  shoulderY: 84, hipY: 271.5, kneeY: 410.25, ankleY: 549
};

/* ---------------- geometry helpers ---------------- */
function _cuLerp(a, b, t) { return a + (b - a) * t; }
function _cuQuadPt(p0, p1, p2, t) {
  const mt = 1 - t;
  return [mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0],
          mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]];
}
function _cuQuadDeriv(p0, p1, p2, t) {
  return [2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]),
          2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])];
}
/* filled tapered ribbon along a quadratic bezier spine p0->p1(ctrl)->p2,
   half-width tapering linearly w0 -> w1. This is what makes a limb one
   continuous shape with no raw joint seam at the elbow/knee. */
function curatorTaperedPath(p0, p1, p2, w0, w1, steps) {
  steps = steps || 20;
  const left = [], right = [];
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const pt = _cuQuadPt(p0, p1, p2, t);
    const d = _cuQuadDeriv(p0, p1, p2, t);
    const len = Math.hypot(d[0], d[1]) || 1;
    const nx = -d[1] / len, ny = d[0] / len;
    const w = _cuLerp(w0, w1, t);
    left.push([pt[0] + nx * w, pt[1] + ny * w]);
    right.push([pt[0] - nx * w, pt[1] - ny * w]);
  }
  const pts = left.concat(right.reverse());
  return "M " + pts.map(p => p[0].toFixed(1) + "," + p[1].toFixed(1)).join(" L ") + " Z";
}
function _cuRotPts(pts, rot, scale) {
  const rad = (rot || 0) * Math.PI / 180, cr = Math.cos(rad), sr = Math.sin(rad), s = scale === undefined ? 1 : scale;
  return pts.map(([x, y]) => [(x * cr - y * sr) * s, (x * sr + y * cr) * s]);
}
function _cuPathFromPts(pts) {
  return "M " + pts.map(p => p[0].toFixed(1) + "," + p[1].toFixed(1)).join(" L ") + " Z";
}
/* three fixed hand shapes, ~20px, tapered wedges (never dots), local
   space centered at the wrist attach point, unrotated pointing "down". */
function curatorHandPath(shape, rot, scale) {
  let pts;
  if (shape === "flat") pts = [[-9, -13], [9, -13], [11, 4], [6, 15], [-6, 15], [-11, 4]];
  else if (shape === "pinch") pts = [[-6, -14], [6, -14], [8, -2], [3, 6], [5, 15], [-5, 15], [-3, 6], [-8, -2]];
  else pts = [[-10, -10], [10, -10], [13, 3], [8, 13], [-8, 13], [-13, 3]]; // grip
  return _cuPathFromPts(_cuRotPts(pts, rot, scale));
}
/* ~14px-wide forward-angled foot wedge, local space at the ankle. */
function curatorFootPath(rot, mirror) {
  const m = mirror === undefined ? 1 : mirror;
  const pts = [[-6, -7], [2, -7], [34 * m, -2], [34 * m, 4], [-6, 7]];
  return _cuPathFromPts(_cuRotPts(pts, rot, 1));
}
/* single continuous hair mass (never cloned shapes), swept to one side. */
function curatorHairPath(cxH, cyH) {
  return `M ${(cxH - 27).toFixed(1)},${(cyH - 6).toFixed(1)} ` +
    `C ${(cxH - 30).toFixed(1)},${(cyH - 34).toFixed(1)} ${(cxH - 6).toFixed(1)},${(cyH - 40).toFixed(1)} ${(cxH + 10).toFixed(1)},${(cyH - 33).toFixed(1)} ` +
    `C ${(cxH + 26).toFixed(1)},${(cyH - 27).toFixed(1)} ${(cxH + 30).toFixed(1)},${(cyH - 6).toFixed(1)} ${(cxH + 22).toFixed(1)},${(cyH + 10).toFixed(1)} ` +
    `C ${(cxH + 18).toFixed(1)},${(cyH + 18).toFixed(1)} ${(cxH + 10).toFixed(1)},${(cyH + 8).toFixed(1)} ${(cxH + 8).toFixed(1)},${(cyH - 2).toFixed(1)} ` +
    `C ${(cxH + 4).toFixed(1)},${(cyH - 16).toFixed(1)} ${(cxH - 14).toFixed(1)},${(cyH - 20).toFixed(1)} ${(cxH - 22).toFixed(1)},${(cyH - 10).toFixed(1)} ` +
    `C ${(cxH - 26).toFixed(1)},${(cyH - 4).toFixed(1)} ${(cxH - 27).toFixed(1)},${(cyH + 2).toFixed(1)} ${(cxH - 24).toFixed(1)},${(cyH + 10).toFixed(1)} Z`;
}
/* explicit neck construction -- never a butt-join between head and torso. */
function curatorNeckPath(cx, y0, y1, w) {
  w = w || 9;
  return `M ${(cx - w).toFixed(1)},${y1.toFixed(1)} L ${(cx - w + 2).toFixed(1)},${y0.toFixed(1)} ` +
    `L ${(cx + w - 2).toFixed(1)},${y0.toFixed(1)} L ${(cx + w).toFixed(1)},${y1.toFixed(1)} Z`;
}
/* one continuous ovoid overcoat/wrap silhouette, shoulder to mid-thigh. */
function curatorCoatPath(cx, shoulderY, hemY, lean) {
  lean = lean || 0;
  const topW = 46, waistY = shoulderY + (hemY - shoulderY) * 0.46, waistW = 30, hemW = 58;
  return `M ${(cx - topW + lean).toFixed(1)},${shoulderY.toFixed(1)} ` +
    `C ${(cx - topW - 6 + lean).toFixed(1)},${(shoulderY + 40).toFixed(1)} ${(cx - waistW - 10).toFixed(1)},${(waistY - 20).toFixed(1)} ${(cx - waistW).toFixed(1)},${waistY.toFixed(1)} ` +
    `C ${(cx - waistW + 4).toFixed(1)},${(waistY + 40).toFixed(1)} ${(cx - hemW + 6).toFixed(1)},${(hemY - 30).toFixed(1)} ${(cx - hemW).toFixed(1)},${hemY.toFixed(1)} ` +
    `L ${(cx + hemW).toFixed(1)},${hemY.toFixed(1)} ` +
    `C ${(cx + hemW - 6).toFixed(1)},${(hemY - 30).toFixed(1)} ${(cx + waistW - 4).toFixed(1)},${(waistY + 40).toFixed(1)} ${(cx + waistW).toFixed(1)},${waistY.toFixed(1)} ` +
    `C ${(cx + waistW + 10).toFixed(1)},${(waistY - 20).toFixed(1)} ${(cx + topW + 6 - lean).toFixed(1)},${(shoulderY + 40).toFixed(1)} ${(cx + topW - lean).toFixed(1)},${shoulderY.toFixed(1)} ` +
    `C ${(cx + 18).toFixed(1)},${(shoulderY - 6).toFixed(1)} ${(cx - 18).toFixed(1)},${(shoulderY - 6).toFixed(1)} ${(cx - topW + lean).toFixed(1)},${shoulderY.toFixed(1)} Z`;
}

/* ---------------- defs (coat gradient) ---------------- */
function ensureCuratorDefs(stage) {
  if (document.getElementById("curatorCoatGrad")) return;
  const defs = el(stage, "defs", {});
  const grad = el(defs, "linearGradient", { id: "curatorCoatGrad", x1: 0, y1: 0, x2: 0, y2: 1 });
  el(grad, "stop", { offset: "0%", "stop-color": CURATOR_COLORS.garmentLight });
  el(grad, "stop", { offset: "100%", "stop-color": CURATOR_COLORS.garmentDark });
}

/* ---------------- build + pose ---------------- */
function makeCurator(parent, opts) {
  const o = opts || {};
  const bodyFill = o.darkKey ? CURATOR_COLORS.taupeDark : CURATOR_COLORS.taupe;
  const g = el(parent, "g", {});
  const c = {
    g, bodyFill,
    legBack: el(g, "path", { fill: bodyFill }),
    footBack: el(g, "path", { fill: bodyFill }),
    legFront: el(g, "path", { fill: bodyFill }),
    footFront: el(g, "path", { fill: bodyFill }),
    neck: el(g, "path", { fill: bodyFill }),
    coat: el(g, "path", { fill: "url(#curatorCoatGrad)" }),
    hairline: el(g, "line", { stroke: CURATOR_COLORS.bronze, "stroke-width": 2.4, "stroke-linecap": "round" }),
    armBack: el(g, "path", { fill: bodyFill }),
    handBack: el(g, "path", { fill: bodyFill }),
    armFront: el(g, "path", { fill: bodyFill }),
    handFront: el(g, "path", { fill: bodyFill }),
    headG: el(g, "g", {})
  };
  c.headEl = el(c.headG, "ellipse", { rx: CURATOR_L.headRx, ry: CURATOR_L.headRy, fill: bodyFill });
  c.hairEl = el(c.headG, "path", { fill: CURATOR_COLORS.garmentDark, opacity: 0.92 });
  return c;
}

/* poseCurator: places the whole figure at stage coords (x,y) -- the
   figure's local origin is the TOP OF THE HEAD -- and applies a pose
   dict: {head_tilt, lean, legs:{back:{},front:{}}, arms:{back:{},front:{}}}.
   Per-limb keys: *_dx/*_dy offsets from the limb's default anchor;
   hand/hand_rot/hand_ox/hand_oy for hands; foot_rot/foot_mirror for feet. */
function poseCurator(c, opts) {
  const pose = opts.pose || {};
  const cx = 0;
  const shoulderY = CURATOR_L.shoulderY, hipY = CURATOR_L.hipY,
        kneeY = CURATOR_L.kneeY, ankleY = CURATOR_L.ankleY;
  const headTop = pose.head_top || 0;
  const tilt = pose.head_tilt || 0;
  const lean = pose.lean || 0;
  const legs = pose.legs || {};
  const arms = pose.arms || {};

  ["back", "front"].forEach((side) => {
    const sign = side === "back" ? -1 : 1;
    const leg = legs[side] || {};
    const hipPt = [cx + sign * 18 + (leg.hip_dx || 0), hipY + (leg.hip_dy || 0)];
    const kneePt = [cx + sign * 16 + (leg.knee_dx || 0), kneeY + (leg.knee_dy || 0)];
    const anklePt = [cx + sign * 14 + (leg.ankle_dx || 0), ankleY + (leg.ankle_dy || 0)];
    const legEl = side === "back" ? c.legBack : c.legFront;
    const footEl = side === "back" ? c.footBack : c.footFront;
    legEl.setAttribute("d", curatorTaperedPath(hipPt, kneePt, anklePt, 8, 5));
    footEl.setAttribute("d", curatorFootPath(leg.foot_rot || 0, leg.foot_mirror === undefined ? 1 : leg.foot_mirror));
    footEl.setAttribute("transform", `translate(${anklePt[0].toFixed(1)},${(anklePt[1] + 7).toFixed(1)})`);
  });

  c.neck.setAttribute("d", curatorNeckPath(cx, shoulderY, 66 + headTop, 9));

  const coatTop = shoulderY - 4, coatHem = hipY + 70;
  c.coat.setAttribute("d", curatorCoatPath(cx, coatTop, coatHem, lean));
  const waistY = coatTop + (coatHem - coatTop) * 0.46;
  c.hairline.setAttribute("x1", cx - 4); c.hairline.setAttribute("y1", waistY - 8);
  c.hairline.setAttribute("x2", cx - 4); c.hairline.setAttribute("y2", waistY + 34);

  ["back", "front"].forEach((side) => {
    const sign = side === "back" ? -1 : 1;
    const arm = arms[side] || {};
    const shPt = [cx + sign * 40 + (arm.sh_dx || 0), shoulderY + 6 + (arm.sh_dy || 0)];
    const elPt = [cx + sign * 40 + (arm.el_dx || 0), shoulderY + (arm.el_dy === undefined ? 110 : arm.el_dy)];
    const wrPt = [cx + sign * 40 + (arm.wr_dx || 0), shoulderY + (arm.wr_dy === undefined ? 210 : arm.wr_dy)];
    const armEl = side === "back" ? c.armBack : c.armFront;
    const handEl = side === "back" ? c.handBack : c.handFront;
    armEl.setAttribute("d", curatorTaperedPath(shPt, elPt, wrPt, 8, 5));
    const hx = wrPt[0] + (arm.hand_ox || 0), hy = wrPt[1] + (arm.hand_oy === undefined ? 10 : arm.hand_oy);
    handEl.setAttribute("d", curatorHandPath(arm.hand || "flat", arm.hand_rot || 0, 1));
    handEl.setAttribute("transform", `translate(${hx.toFixed(1)},${hy.toFixed(1)})`);
  });

  const headCx = cx, headCy = headTop + 33;
  c.headEl.setAttribute("cx", headCx); c.headEl.setAttribute("cy", headCy);
  c.hairEl.setAttribute("d", curatorHairPath(headCx, headCy));
  c.headG.setAttribute("transform", `rotate(${tilt.toFixed(2)} ${headCx} ${headCy})`);

  c.g.setAttribute("transform", `translate(${(opts.x || 0).toFixed(1)},${(opts.y || 0).toFixed(1)}) scale(${opts.scale === undefined ? 1 : opts.scale})`);
}

/* recursive numeric lerp between two pose dicts of the same shape --
   convenience for authoring transitions between two named poses.
   Non-numeric leaves (hand shape strings) snap at k=0.5. */
function lerpCuratorPose(a, b, k) {
  if (typeof a === "number" && typeof b === "number") return _cuLerp(a, b, k);
  if (a && b && typeof a === "object" && typeof b === "object") {
    const out = {};
    const keys = new Set(Object.keys(a).concat(Object.keys(b)));
    keys.forEach((key) => { out[key] = lerpCuratorPose(a[key], b[key], k); });
    return out;
  }
  return k < 0.5 ? a : b;
}

/* four named reference poses, carried over 1:1 from the static reference
   sheet (curator_mk2_sheet.png, preview-only, not committed) -- author
   new poses by copying one of these and nudging numbers. */
const CURATOR_POSES = {
  regard: {
    head_tilt: 6, lean: -4,
    legs: {
      back: { hip_dx: -2, knee_dx: -4, ankle_dx: -2 },
      front: { hip_dx: 6, knee_dx: 14, ankle_dx: 10, foot_rot: 8 }
    },
    arms: {
      back: { el_dx: -6, el_dy: 112, wr_dx: -10, wr_dy: 208, hand: "flat" },
      front: { el_dx: 8, el_dy: 110, wr_dx: 6, wr_dy: 206, hand: "flat" }
    }
  },
  reach: {
    head_tilt: -4, lean: 10,
    legs: {
      back: { hip_dx: -4, knee_dx: -8, ankle_dx: -6 },
      front: { hip_dx: 4, knee_dx: 6, ankle_dx: 4 }
    },
    arms: {
      back: { el_dx: -10, el_dy: 108, wr_dx: -16, wr_dy: 200, hand: "flat" },
      front: { el_dx: 70, el_dy: 70, wr_dx: 140, wr_dy: 50, hand: "pinch", hand_rot: -30, hand_ox: 6, hand_oy: 0 }
    }
  },
  draw: {
    head_tilt: 3, lean: -8,
    legs: {
      back: { hip_dx: -6, knee_dx: -10, ankle_dx: -14, foot_rot: -6 },
      front: { hip_dx: 8, knee_dx: 10, ankle_dx: 6 }
    },
    arms: {
      back: { el_dx: -4, el_dy: 110, wr_dx: -8, wr_dy: 204, hand: "flat" },
      front: { el_dx: 44, el_dy: 96, wr_dx: -10, wr_dy: 96, hand: "grip", hand_rot: 90, hand_ox: 0, hand_oy: 0 }
    }
  },
  liftAndTilt: {
    head_tilt: -8, lean: 6,
    legs: {
      back: { hip_dx: -2, knee_dx: -6, ankle_dx: -4 },
      front: { hip_dx: 6, knee_dx: 12, ankle_dx: 8 }
    },
    arms: {
      back: { el_dx: -8, el_dy: 112, wr_dx: -12, wr_dy: 206, hand: "flat" },
      front: { el_dx: 48, el_dy: 60, wr_dx: 30, wr_dy: -10, hand: "pinch", hand_rot: 20, hand_ox: 0, hand_oy: -4 }
    }
  }
};
