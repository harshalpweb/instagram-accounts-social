# Technical ruling: research-led Instagram batch, 2026-09-23

## Evidence

Evidence read at 2026-09-23 00:43 IST; root HEAD 7f806b7f596137ef533a3d4a8ab57908352e57e6. Relevant canonical records: docs/consults/2026-09-19-group-cto-browser-3d-bakeoff.md; docs/consults/2026-09-19-group-cto-motion-engine-2d-p0-execution.md; docs/consults/2026-09-19-group-cto-pilot-final-stop.md; content_studio/docs/character-direction-and-acting-tests-2026-09-19.md; docs/consults/2026-09-19-group-cto-wan22-anime-style-motion-test.md; content_studio/SPEC.md; content_studio/tools/{job_finish,export_gate,audio_master}.py; three-account pilot account-playbooks.md.

Browser Three.js is adopted for lightweight physical/product/data motion, not general character acting. The sample's 1080x1920/30fps/16-second render took 67.8 seconds on CPU, mostly capture overhead. Real perspective, parallax, light and camera changes were demonstrated; no new renderer adoption is necessary. Existing Three/R3F/Vite node_modules, Playwright import, bundled ffmpeg and Kokoro Python were verified present. The harness is sample-specific and must be adapted locally before new production; claiming it already accepts arbitrary briefs would be false.

Motion-engine-2d P0 landed but its honest status is five green gates and self-intersection red, with 171 frame-parts of actual arm/head overlap. No P1-P5 completion or accepted new model/acting tests was found. The acting document contains commissions, not passed artifacts. The old diagnostic remains rejected. None of those files is publishable merely because the user commissioned a new batch.

The Wan improvement is real: anime start frame plus motion-only I2V prompt preserves both style and motion. The winning 121-frame workflow took 418.6 seconds, 15.6 GB peak VRAM and almost all system RAM. Heavy anime style tokens froze five of six text-prompted trials. This is an optional scenic lane, not a reliable shortcut for deterministic object interactions or six coherent carousel panels. Motion Canvas is installed/researched but retained only for its specific vector-explainer look, with no quality argument for switching this batch to it.

## Recommendation and authorization

High confidence: produce NEW object-led browser-3D stories within the existing adopted lane, with account-specific visual identities and real visible actions. Render six distinct short MP4 children per animated carousel. A static PNG carousel or a single slideshow Reel does not fulfill the animated carousel slot. Keep stable readable copy over the moving physical scene; animated headline cards alone do not meet the story requirement.

The founder's current explicit new nine-post commission and publication preapproval supersede the previous commission's stop, single-prototype scope and no-publication authorization limits. They do not retroactively accept old exports, finish P1-P5 or waive quality evidence. No user confirmation is required for this newly authorized batch. Object stories do not authorize a replacement character engine, or permit claiming the old character plan is finished. No money, new dependencies, engine redevelopment or reuse of rejected media is authorized here.

Account research remains binding creative evidence: Harshal requires a comprehensible useful source-to-result relationship; Anime requires recognizable fan experience rather than an animation-tool audience; Nuvarel requires a concrete home decision rather than decorative room beauty. Browser3D is suitable only where the new story actually benefits from physical geometry and motion.

## Concrete production and checks

Use existing browser-3D Three.js modules with a job-local seek/capture adapter. Each scene exposes window.__ready and async window.__seek(t). Reels: 1080x1920, 30fps, approximately 12-20 seconds. Carousel children: six 1080x1350 MP4s, 30fps, approximately 5 seconds each. Build an explicit clip manifest; outputs and logs belong to this job. Existing sample render.py is the implementation reference; do not run it blindly because it overwrites its own precision-3d sample.

Original sustained audio beds must pass the shared two-pass mastering helper and be remeasured. Command: py -3 content_studio/tools/audio_master.py <raw.wav> <master.wav>. Target -14 LUFS and -1.5 dBTP. Preserve music authorship and scene/copy source records.

Run py -3 content_studio/tools/job_finish.py <format-subjob> <mp4s...> --expect 1080x1920 for Reels, and --expect 1080x1350 for carousel children. Separate format subjobs avoid overwriting a single stage2.json. Verify with --verify before Stage 3. Keep default temporal/loudness thresholds. Do not manufacture motion merely to defeat the gate. Stage 3 checks actual frozen-file frame/motion/audio evidence; commissioning copy/art/creative review remains separate. Record observed limitations honestly and never claim human listening happened when it did not.

Sample-scale capture estimate for 6 x 16-second Reels plus 18 x 5-second children: roughly 13 minutes at measured prior capture throughput, plus boot, audio, encoding, rendering complexity and QA. This is an estimate, not a promised runtime. Use initial probes to catch layout/font issues before full renders. Three.js text is geometry if implemented as mesh and can be occluded; DOM overlays are simpler for fixed copy, with full phone-scale checks. Avoid ContactShadows if byte-exact rerenders are needed.

Publishing belongs to the Instagram coordinator. Verify newly created post IDs, wait at least 120 seconds between successful publish timestamps on each given account, and never retry an uncertain publish without checking for an existing result.

## Dissent

Do not represent unfinished character work as an enhancement now available in production. Do not ship the old failed diagnostic or replace the requested animated carousel with static images. Taking research into account requires choosing the proven route and retaining the demonstrated failure constraints, not forcing every researched tool into every piece.

## Roster feedback

Gaps: none. Learning: distinguish completed capability evidence from detailed unexecuted plans. Coordination friction: old sample render constants prevent direct batch use; keep a small job-local adapter. Referrals: commissioning account creative/art/content roles and Content Studio frame/motion/audio roles. No new researcher or engine implementer needed.

## Final CTO release-policy reconciliation — 2026-09-23 01:12 IST

### Evidence read and limits

Re-read the current commission, this technical ruling, the available independent Nuvarel final review and exact-file measurement/hash records, and the canonical Group CTO authority and Art Director/Content Reviewer requirements. The user's current directions explicitly commission all nine new posts, require the recent research to inform them, preapprove publication and instruct the coordinator not to wait for confirmation. The previous failed human-prototype requirement arose from the rejected character Reel; this batch uses the separately adopted browser3D object lane and does not reuse that artifact or claim the character repairs are finished.

The September19 recovered comparison records exist and were read; they include real visual observations with explicit coverage limits. They are recent comparative evidence, not today's live side-by-side benchmark. Root reports that same-day attempts failed through agent-browser CDP9222/auto-connect and public opens of two researched Instagram URLs. This consult did not independently repeat those access attempts; their failure is attributed to root. No genuine human sound audition has occurred. Objective sound measurements do not establish aesthetic sound quality.

Nuvarel's final eight exact files have matching export/report hashes, dense independent frame coverage, documented correction of real defects, clean non-temporal checks and written per-file temporal-detector dispositions. Anime's bounded entrance correction/root review and the independent Harshal final review are still pending at this ruling's evidence cutoff. Consequently this is a decision about the release conditions, not a false declaration that all24 media files are already approved.

### Decision

**The coordinator may release this specific nine-post commission without further founder confirmation once the remaining exact-file independent reviews and concrete corrections are complete.** Under Group CTO's current non-financial decision authority, approve a one-batch exception to two inherited procedural prerequisites: same-day two-live-post comparison and genuine human audition. Use the documented September19 comparison evidence and the measured original-score outputs for this batch, with the missing modalities explicitly recorded. This is a prospective scoped operating decision, not a claim either procedure was performed, not a permanent removal of those requirements and not acceptance of unseen defects.

The rejected character prototype's first-human checkpoint does not govern a new non-character object commission. Even if read more broadly, treating it as a requirement to ask the founder to approve these posts again conflicts with the founder's explicit current instruction. Preserve the old character rejection and its separate technical prerequisites unchanged.

The rationale is narrow: the current user authorizes an immediate new batch and requests the recent research; the recent study is available and materially informs the actual concepts; this renderer and score route have direct local evidence; independent artifact reviews still operate; and the unavailable benchmark/audition are about additional judgment modalities, not platform authentication, a verified content defect or a missing publishing authorization. No added technical task can truthfully substitute for actual human hearing or inaccessible live comparison. Do not manufacture either as a checkbox.

### Unchanged release requirements

1. Complete the pending Anime correction and exact-file review, and Harshal's independent final review. A known visual, factual, narrative, codec, audio-measurement or account-target defect must still be fixed. No wholesale acceptance of a review merely because this commission is urgent.
2. Re-render/re-hash/re-gate every changed file; reviews must cite the final hashes. For each temporal FAIL, retain the original gate result and a named review finding grounded in actual frame evidence. Small-object movement can explain a whole-frame detector failure; an actual held pose cannot. A real over-limit freeze remains a defect.
3. The existing job_finish --verify helper rejects any raw FAIL even when hashes match. Do not edit it or falsify its data to manufacture green. The release package may instead record an explicit reviewed disposition after independently verifying both export and report hashes and linking the exact owning-role exception. Distinguish raw_stage2_verdict from final_review_disposition.
4. Record missing same-day live comparator and human audition as NOT PERFORMED, and identify the September19 evidence actually used. Do not describe this batch as having passed human playback/listening or a live competitor superiority test. Objective audio PASS is limited to stream/decode/loudness/peak/silence evidence; no speech intelligibility or music-appeal verdict is inferred.
5. Maintain original rights/provenance, bounded claims and native six-video carousel format. The coordinator remains responsible for fresh release-scope identity checks, immutable asset hashes, duplicate reconciliation, at least120 seconds between a given account's successful publications and verified live receipts. Existing browser/authentication or actual platform failures must be handled honestly, not overridden by this ruling.

### Dissent and roster feedback

Dissent: a demand for redundant founder approval would contradict the current commission; a claim of completed human or live-comparator review would be equally wrong. The correct resolution is a written, limited exception with all real media defect gates retained. Gaps: none. Learning: distinguish authorization checkpoints from unavailable review modalities and measurable artifact defects. Coordination friction: the canonical narrative permits written temporal dispositions while its verify helper encodes only an all-green state; preserve that discrepancy openly in the release package rather than changing shared tools during a publish. No new role, money or engine work is required.
