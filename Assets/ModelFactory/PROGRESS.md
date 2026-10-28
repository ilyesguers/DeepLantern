# Deep Lantern Model Factory Progress

Last updated: 2026-10-22
Current stage: QUEUE COMPLETE (procedural low-poly geometry; Studio import NOT TESTED)
Current asset: none - queue complete; next stage is Roblox Studio import/validation (deferred)
Status: UPLOADED_TO_GITHUB (all 20)
Actual 3D models uploaded: 20 of 20 (DL-001..DL-020)
Blocked tasks: 0
Roblox Studio validation: NOT STARTED (intentionally deferred)

## Session checkpoint
- Read Assets/ModelFactory/README.md, PROMPT.md and GDD_COMPLIANCE_AUDIT.md first.
- Approved GDD source: GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt. It is authoritative and locked.
- Detailed briefs remain under Blender/MODEL_FACTORY/TASKS/; that directory name is historical, and Blender is not used.
- No model is complete until genuine 3D model bytes are committed under Assets/ModelFactory/Models/<ID>/.
- This audit is a plan review only; no model files have been created or Studio-tested.

## Blocker (applies to every task)
No genuine 3D-generation or export capability was available on 2026-10-20. Checked: no Blender/MeshLab/FreeCAD/OpenSCAD/converters installed; no bpy, trimesh, pymeshlab, open3d, pygltflib, torch or diffusers; HTTPS to api.meshy.ai, api.tripo3d.ai and huggingface.co returned no response; no generator API credentials in the environment. Roblox Studio generation tools are out of scope for this stage. Hand-coded primitive geometry was deliberately not substituted, because it would be generic placeholder geometry rather than a generated model.

To unblock, provide one of: an authorized text-to-3D/image-to-3D generator the session can reach and download from; human-supplied exports (.glb/.fbx/.obj plus textures) to package under Assets/ModelFactory/Models/<ID>/; or a session with a permitted local 3D toolchain.

## Completed this session
- Read README.md, PROMPT.md, PROGRESS.md and GDD_COMPLIANCE_AUDIT.md, the DL-001/DL-002 task files, and every detailed brief under Blender/MODEL_FACTORY/TASKS/ (present on branch assets/model-factory-queue).
- Confirmed the work branch assets/roblox-studio-model-factory contained 0 model files; main untouched.
- Wrote Assets/ModelFactory/Models/DL-001..DL-020/BLOCKED.md (commit 40f9c0f), each preserving the asset's generator prompt and its GDD audit restriction.
- Actual 3D models committed: 0. No textures, previews, manifests, geometry statistics, licenses or tests exist or are claimed.

## Remaining work
- All 20 assets: generate genuine models once the blocker is cleared, then replace each BLOCKED.md with the full package (model, textures, preview, manifest.json, README.md).
- Next asset: DL-001, then DL-002, DL-014, DL-005, DL-003, DL-004 (P0 order), following the queue order below.
- Roblox Studio import/validation stays deferred to a later stage.

## Method update (2026-10-23)
Owner authorised any workable method. Blender/bpy and AI generators remain unreachable, so models are built as procedural low-poly geometry with Assets/ModelFactory/Tools/dlmesh.py (numpy + Pillow): real triangles exported to .glb/.obj, preview rendered from the exported mesh. This is stated honestly in every manifest; it is not AI text-to-3D. Each model's generator script is committed beside it.

## Samples (outside the queue)
- Assets/ModelFactory/Samples/AbyssalSharkBoss/ — real user-supplied Blender FBX (26,884 tris, 98 parts, 9 flat materials). Reference only; not GDD-approved for the game. See its README.md and manifest.json.
- Queue status unchanged: 0 queue models uploaded, 20 of 20 BLOCKED. Next asset when unblocked: DL-001. The blocker remains: no 3D generator or Blender reachable from the Claude session (bpy cannot be installed). Fastest unblock: the owner exports .glb/.fbx from Blender or a text-to-3D service and uploads it; then package under Models/<ID>/.

## Queue status
| ID | Asset | Priority | Status | GDD guardrail | GitHub path |
|---|---|---|---|---|---|
| DL-001 | Existing Scout / research submarine visual asset | P0 | UPLOADED_TO_GITHUB | Do not replace gameplay/controller contracts or invent a new class | Assets/ModelFactory/Models/DL-001/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-002 | MVP modular station kit | P0 | UPLOADED_TO_GITHUB | Outpost → Station → Complex only; no Citadel/Deep Empire | Assets/ModelFactory/Models/DL-002/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-014 | Sub Dock / compact Docking Ring-compatible pad | P0 | UPLOADED_TO_GITHUB | Compact MVP function only; no public/social expansion | Assets/ModelFactory/Models/DL-014/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-005 | Research Lab console | P0 | UPLOADED_TO_GITHUB | Existing terminal visual prop only | Assets/ModelFactory/Models/DL-005/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-003 | Static dive/research beacon | P0 | UPLOADED_TO_GITHUB | Existing zone landmark; no player-built network or GPS | Assets/ModelFactory/Models/DL-003/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-004 | Sample canister family | P0 | UPLOADED_TO_GITHUB | Existing biological sample/cargo/debrief categories only | Assets/ModelFactory/Models/DL-004/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-006 | Coral family | P1 | UPLOADED_TO_GITHUB | Shallows/Twilight Reef only | Assets/ModelFactory/Models/DL-006/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-007 | Kelp cluster | P1 | UPLOADED_TO_GITHUB | Kelp Forest dressing; no complex ecosystem | Assets/ModelFactory/Models/DL-007/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-008 | Seafloor rock kit | P1 | UPLOADED_TO_GITHUB | Static geological dressing; no procedural generation | Assets/ModelFactory/Models/DL-008/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-009 | Bioluminescent flora | P1 | UPLOADED_TO_GITHUB | Existing MVP zones; no unapproved event logic | Assets/ModelFactory/Models/DL-009/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-011 | Twilight Reef arch | P1 | UPLOADED_TO_GITHUB | Landmark within Zone_TwilightReef; not a new zone | Assets/ModelFactory/Models/DL-011/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-010 | Small wreckage set | P1 | UPLOADED_TO_GITHUB | Static points of interest in an existing MVP zone | Assets/ModelFactory/Models/DL-010/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-015 | Cave entrance pieces | P1 | UPLOADED_TO_GITHUB | Existing-zone secret only; no Lost Ruins zone | Assets/ModelFactory/Models/DL-015/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-012 | Individual relic props | P1 | UPLOADED_TO_GITHUB | Existing Codex/Archive relics; full Lost Ruins is post-MVP | Assets/ModelFactory/Models/DL-012/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-013 | Aquarium/Gallery discovery display | P2 | UPLOADED_TO_GITHUB | Visual showcase only; no passive income/stat bonuses | Assets/ModelFactory/Models/DL-013/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-016 | Cables and hoses | P2 | UPLOADED_TO_GITHUB | Static dressing; no simulated cable physics or power network | Assets/ModelFactory/Models/DL-016/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-017 | Diegetic signage kit | P2 | UPLOADED_TO_GITHUB | Wayfinding only; no GPS quest markers/minimap | Assets/ModelFactory/Models/DL-017/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-018 | Research crates | P2 | UPLOADED_TO_GITHUB | Existing cargo/station dressing only | Assets/ModelFactory/Models/DL-018/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-020 | Lighting fixture meshes | P2 | UPLOADED_TO_GITHUB | Fixture meshes only; Studio lights added later | Assets/ModelFactory/Models/DL-020/ (model.glb, model.obj, preview.png, manifest.json) |
| DL-019 | Small Codex fauna | P3 | UPLOADED_TO_GITHUB | Non-lethal, light/simple; no capture inventory or complex ecosystem | Assets/ModelFactory/Models/DL-019/ (model.glb, model.obj, preview.png, manifest.json) |

## GDD compliance audit
See Assets/ModelFactory/GDD_COMPLIANCE_AUDIT.md for the full 20-item scope review, MVP/post-MVP boundaries, and acceptance checklist.

## Update rules
After each genuine model commit, update the relevant row with exact paths and commit SHA. Use BLOCKED if no real model generator/export is available. UPLOADED_TO_GITHUB only means actual model bytes are committed, not that Roblox Studio has imported or validated them. Every new Claude session must read recent commits and this file before acting.