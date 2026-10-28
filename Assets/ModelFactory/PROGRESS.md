# Deep Lantern Model Factory Progress

Last updated: 2026-10-27
Current stage: v2 geometry exports exist for DL-001..DL-020; DL-001 reopened for review
Current asset: DL-001 Scout / research submarine
Status: DL-001 NEEDS_REVIEW; other assets have committed v2 exports with file measurements recorded in their manifests
Actual 3D models uploaded: 20 of 20 (DL-001..DL-020)
Blocked tasks: DL-001 geometry correction is blocked in this session by the missing local Python/3D toolchain and no connected Roblox Studio
Roblox Studio validation: NOT TESTED for all 20

## Current session handoff (2026-10-27)
- Starting commit on `main`: `8a2f69df3f8524482faecf69f8cd67a0cd7e7c5e` (v2 quality pass for DL-001..DL-020). No model export was changed in this session.
- DL-001 baseline: v1 export from `319b25270be6d14ac3cb06caa1cfc9b8736fcc71`; v2 export from `8a2f69df3f8524482faecf69f8cd67a0cd7e7c5e`.
- DL-001 status: `NEEDS_REVIEW`. The v2 preview improves surface finish and adds readable structural detail, but review found the static nose beam stretches the full export bounds to 15.694 m (the hull itself is about 8.53 m long), exceeding the 8 m design length. The hull height is 3.851 m against the 3.1 m design target; side pods remain partly hidden in side view; the preview's repeated texture pattern is visually busy. Do not treat the extra beam as vehicle geometry or scale the whole model to compensate.
- Independent file check in this session: v1 and v2 GLB containers parsed; v1 = 175,300 bytes / 2,032 triangles / 5 meshes and materials / 0 textures / 4.28 x 3.76 x 8.53 m; v2 = 943,212 bytes / 6,254 triangles / 9 meshes and materials / 2 embedded textures / 4.28 x 3.851 x 15.6941 m. The v2 values match its manifest. Both exports have finite accessor bounds. Genuine software previews were compared; they are not Studio renders.
- v2 improvements already present: chamfered structural edges, baked vertex AO, smoothed normals, UVs, procedural detail maps, and improved lighting in the software preview. These completed changes must not be regenerated or overwritten.
- Not completed here: no new geometry or export, no Studio import, collision, in-game lighting, controller alignment, mobile performance or gameplay-distance validation. Python resolves only to the WindowsApps placeholder; Blender is absent, the Python download probe timed out, and the connected Studio list is empty.
- Next required action: with a working Python + NumPy/Pillow toolchain (or another authorized exporter), make a focused DL-001 candidate that removes or shortens the optional beam, brings the hull height toward 3.1 m without scaling the FX, improves side-pod visibility, and reduces overly busy texture contrast. Preserve v2 as baseline, regenerate model/preview/manifest together, then compare and run file checks. Studio validation remains a separate later gate.
- All 19 other assets have v2 files in the same commit, but their previews and gameplay fit were not independently reviewed in this session. Do not repeat the committed v2 pass; continue with DL-001 until its specific issues are resolved, then audit DL-002.

## Project references
- The approved source is `GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt`; `Assets/ModelFactory/GDD_COMPLIANCE_AUDIT.md` records each asset's scope guardrail.
- The model pipeline is procedural Python geometry using `Assets/ModelFactory/Tools/dlmesh.py` with NumPy and Pillow. It is not AI text-to-3D or Blender sculpting.
- Model export status, file-level checks, visual review, and Studio validation are separate gates. A software preview is not an in-engine result.

## Historical checkpoints
- Earlier 2026-10-20 notes marked the queue blocked before a usable procedural pipeline was committed; later commits superseded that state.
- Commits `319b252`, `5336728`, `c0ab058`, `2a07848`, and `7246baf` added genuine model exports for all 20 IDs.
- Commit `8a2f69d` on `main` applied the v2 geometry/texture/preview pass to all 20 and re-measured the GLBs. The current session independently parsed and compared DL-001 only.

## Queue status
| ID | Asset | Priority | Status | GDD guardrail | GitHub path |
|---|---|---|---|---|---|
| DL-001 | Existing Scout / research submarine visual asset | P0 | NEEDS_REVIEW | Do not replace gameplay/controller contracts or invent a new class | Assets/ModelFactory/Models/DL-001/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-002 | MVP modular station kit | P0 | IMPROVED_FILE_QA_PASSED | Outpost → Station → Complex only; no Citadel/Deep Empire | Assets/ModelFactory/Models/DL-002/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-014 | Sub Dock / compact Docking Ring-compatible pad | P0 | IMPROVED_FILE_QA_PASSED | Compact MVP function only; no public/social expansion | Assets/ModelFactory/Models/DL-014/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-005 | Research Lab console | P0 | IMPROVED_FILE_QA_PASSED | Existing terminal visual prop only | Assets/ModelFactory/Models/DL-005/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-003 | Static dive/research beacon | P0 | IMPROVED_FILE_QA_PASSED | Existing zone landmark; no player-built network or GPS | Assets/ModelFactory/Models/DL-003/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-004 | Sample canister family | P0 | IMPROVED_FILE_QA_PASSED | Existing biological sample/cargo/debrief categories only | Assets/ModelFactory/Models/DL-004/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-006 | Coral family | P1 | IMPROVED_FILE_QA_PASSED | Shallows/Twilight Reef only | Assets/ModelFactory/Models/DL-006/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-007 | Kelp cluster | P1 | IMPROVED_FILE_QA_PASSED | Kelp Forest dressing; no complex ecosystem | Assets/ModelFactory/Models/DL-007/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-008 | Seafloor rock kit | P1 | IMPROVED_FILE_QA_PASSED | Static geological dressing; no procedural generation | Assets/ModelFactory/Models/DL-008/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-009 | Bioluminescent flora | P1 | IMPROVED_FILE_QA_PASSED | Existing MVP zones; no unapproved event logic | Assets/ModelFactory/Models/DL-009/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-011 | Twilight Reef arch | P1 | IMPROVED_FILE_QA_PASSED | Landmark within Zone_TwilightReef; not a new zone | Assets/ModelFactory/Models/DL-011/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-010 | Small wreckage set | P1 | IMPROVED_FILE_QA_PASSED | Static points of interest in an existing MVP zone | Assets/ModelFactory/Models/DL-010/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-015 | Cave entrance pieces | P1 | IMPROVED_FILE_QA_PASSED | Existing-zone secret only; no Lost Ruins zone | Assets/ModelFactory/Models/DL-015/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-012 | Individual relic props | P1 | IMPROVED_FILE_QA_PASSED | Existing Codex/Archive relics; full Lost Ruins is post-MVP | Assets/ModelFactory/Models/DL-012/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-013 | Aquarium/Gallery discovery display | P2 | IMPROVED_FILE_QA_PASSED | Visual showcase only; no passive income/stat bonuses | Assets/ModelFactory/Models/DL-013/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-016 | Cables and hoses | P2 | IMPROVED_FILE_QA_PASSED | Static dressing; no simulated cable physics or power network | Assets/ModelFactory/Models/DL-016/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-017 | Diegetic signage kit | P2 | IMPROVED_FILE_QA_PASSED | Wayfinding only; no GPS quest markers/minimap | Assets/ModelFactory/Models/DL-017/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-018 | Research crates | P2 | IMPROVED_FILE_QA_PASSED | Existing cargo/station dressing only | Assets/ModelFactory/Models/DL-018/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-020 | Lighting fixture meshes | P2 | IMPROVED_FILE_QA_PASSED | Fixture meshes only; Studio lights added later | Assets/ModelFactory/Models/DL-020/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-019 | Small Codex fauna | P3 | IMPROVED_FILE_QA_PASSED | Non-lethal, light/simple; no capture inventory or complex ecosystem | Assets/ModelFactory/Models/DL-019/ (model.glb, model.obj, preview.png, manifest.json) |

## GDD compliance audit
See Assets/ModelFactory/GDD_COMPLIANCE_AUDIT.md for the full 20-item scope review, MVP/post-MVP boundaries, and acceptance checklist.

## Update rules
Status meanings: `IMPROVED_FILE_QA_PASSED` means an improved export and file measurements are recorded; it does not imply visual approval or Studio validation. The v2 commit and per-model manifests are the source for those inherited statuses. `NEEDS_REVIEW` means a concrete visual/proportion issue remains. Every new session should read recent commits and this tracker before acting.

## v2 quality pass (commit 8a2f69d on main)
All 20 models were regenerated with chamfered edges, baked vertex AO, smoothed normals, box-projected UVs, procedural grayscale detail maps, optional static `fx_*` meshes, and improved software previews. DL-001 is 6,254 triangles. Textures are procedural rather than hand-painted; FX are static meshes; DL-019 is unrigged. Roblox Studio import remains NOT TESTED for every asset.

