# Deep Lantern — Model Quality Upgrade Plan

Status: AUDIT / UPGRADE PLAN ONLY. No model geometry has been replaced by this document.
Base: main at the time this branch was created.
Scope: DL-001..DL-020, preserve approved GDD and all gameplay/controller contracts.
Design target: premium, high-detail deep-sea research visuals that remain readable and performant in Roblox, including mobile/low-end devices.

## Rules that cannot be waived
- Never change game scripts, controller contracts, model class names, stats, currencies, zones, or mechanics as part of an art-only upgrade.
- Keep approved GDD Parts 1–10 authoritative; use existing Art/VisualReference references.
- Never overwrite the current production export before a candidate has passed file-level checks. Preserve baseline files and compare before/after.
- Never claim Roblox Studio import, appearance, collision, scale, or performance validation unless it was actually run in Studio.
- A preview image is not a model. A new model is accepted only when real non-empty export bytes, source when available, preview, manifest, and README are committed.
- Keep materials and mesh counts intentional; use texture maps only when they add visible value. Do not add excessive tiny geometry that vanishes at gameplay distance.

## Baseline verified from GitHub
- All 20 model folders currently contain README.md, manifest.json, and preview.png; DL-001 has an editable Python generator source. Other model-specific source/export coverage must be audited before changes.
- The existing generator is procedural Python geometry, not AI text-to-3D or Blender sculpting. It uses numpy/Pillow and exports GLB/OBJ/MTL. This is valid geometry, but it does not automatically mean premium finish.
- DL-001 manifest baseline: model.glb 175,300 bytes; 2,032 triangles; 5 materials; no textures; measured size 8.53 x 4.28 x 3.76 metres. The design reference calls for approximately 8 x 4.2 x 3.1 m. Current file is therefore larger than the reference, especially in height, and needs scale/proportion review.
- DL-001 orientation is recorded as Y-up, nose toward -Z, +X right; pivot is at hull centreline mid-length. Roblox import and alignment with the live submarine root remain unverified.
- DL-001 known visual limitations in its README: no UV/texture detail, no separate moving parts, and side pods partly hidden by the hull in side view.
- DL-002 is a modular station kit with 14 separately exported part files plus a spaced preview layout. Its dimensions, pivots, snapping, module naming and assembly compatibility need a systematic check.
- Existing PROGRESS.md currently says all 20 exports are uploaded, but explicitly says Roblox Studio validation has not started. Preserve that distinction.

## Upgrade order
### P0 — core MVP anchors
1. DL-001 Scout / research submarine — first candidate and before/after review.
2. DL-002 modular station kit.
3. DL-014 compact Sub Dock / Docking Ring-compatible pad.
4. DL-005 Research Lab console.
5. DL-003 static dive/research beacon.
6. DL-004 sample canister family.

### P1 — MVP environment and discovery
DL-006 coral, DL-007 kelp, DL-008 rocks, DL-009 bioluminescent flora, DL-011 Twilight Reef arch, DL-010 small wreckage, DL-015 cave entrance pieces, DL-012 individual relic props.

### P2 — supporting props
DL-013 Gallery display, DL-016 cables/hoses, DL-017 signage, DL-018 research crates, DL-020 lighting fixtures.

### P3 — Codex fauna
DL-019 small non-lethal fauna; keep it simple and defer rigging/animation unless separately scoped and produced.

## DL-001 upgrade acceptance checklist
- Compare the current preview and actual export to Art/VisualReference/02_Submarine_Design.png and the GDD.
- Improve silhouette hierarchy: hull, cockpit/viewports, nose lantern/scanner, side pods, keel/skids, thrusters, service panels, fins and antenna/mast should be readable and not intersect or disappear from key angles.
- Add medium-scale panel seams, access panels, fasteners and functional-looking trim only where they remain readable in game. Avoid floating decals or tiny geometry noise.
- Give glass, painted hull, dark structural metal and emissive lenses distinct material treatment; no claim of texture maps unless files exist.
- Measure proportions against the design sheet; explain any deliberate deviation. Check bounds, triangle counts, material count, normals, degenerate/non-finite vertices and GLB round-trip if a suitable parser is available.
- Record scale, axes and pivot explicitly. Keep current file as baseline until candidate export is verified.
- Export a genuine candidate model and genuine preview from that candidate; update manifest with hashes and measured statistics.
- Do not mark Studio validation complete before a human or connected Studio environment tests import, appearance, scale, materials, collision, mobile rendering and alignment to the existing submarine root.

## Common technical QA for all 20
For each asset, capture: export format and size; bounds/dimensions and units; pivot/orientation; mesh/triangle/material counts when measurable; missing/degenerate/non-finite geometry checks where tooling supports them; texture files and references; licensing/source; preview; Roblox import notes; GDD scope guardrail; known limitations.
For modular assets, additionally check repeatable dimensions, consistent grid/snapping, seams/gaps, naming and whether parts can be assembled without overlapping. For environment dressing, prioritize silhouette variety and reuse over dozens of unique expensive meshes. For fauna, do not add combat, capture inventory, or unapproved AI behavior.

## Completion states
- AUDIT_ONLY: findings recorded; no asset changed.
- CANDIDATE_GENERATED: new export exists on the feature branch; not yet accepted.
- FILE_QA_PASSED: checks actually performed and evidence recorded.
- NEEDS_REVIEW: candidate is committed but human visual review remains.
- STUDIO_VALIDATED: only after Roblox Studio import/visual/performance checks actually run.
- BLOCKED: the exact missing capability is recorded.

## Immediate next action
Create an improved DL-001 candidate while retaining the existing export as baseline. If this session cannot execute the generator and validate its real binary output, stop at the audit and report the exact blocker; do not replace exports with a concept image or claim the upgrade is complete.
