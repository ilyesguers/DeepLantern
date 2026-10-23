# DL-006 — BLOCKED

Asset: DL-006 — Stylized Coral Family
Priority/GDD fit: MVP environment
Date recorded: 2026-10-20
Status: BLOCKED — no model, texture or preview exists for this asset.

## Precise blocker
No genuine 3D-generation or 3D-export capability was available in this session. A real model needs a tool that outputs actual geometry (.glb / .fbx / .obj or similar) from a prompt or source. The capabilities checked were:

- Local 3D software: none installed (no Blender, MeshLab, FreeCAD, OpenSCAD, assimp, glTF/FBX converters). Blender is also excluded by the project rules.
- Python 3D / generative libraries: bpy, trimesh, pymeshlab, open3d, pygltflib, torch and diffusers are not installed. Only numpy, Pillow and matplotlib are present, which cannot generate or export a finished asset on their own.
- Hosted text-to-3D services: HTTPS requests from the session to api.meshy.ai, api.tripo3d.ai and huggingface.co returned no response, and no generator API credentials are present in the environment.
- Roblox Studio: its mesh/texture generation tools are intentionally out of scope for this stage and were not used.

Hand-writing vertex data from code was deliberately not substituted. It would produce generic primitive placeholder geometry, which the acceptance criteria forbid, and it would not be a genuine generated model.

## What unblocks this task
Any one of: (a) an authorized text-to-3D or image-to-3D generator the session can reach and download from, (b) a human-supplied model export (.glb/.fbx/.obj plus textures) dropped into this folder for packaging, or (c) a session with a permitted local 3D toolchain.

## GDD scope that still applies
Audit row for DL-006 (Coral family):

Place only in Shallows/Twilight Reef where appropriate. Use reusable silhouettes; avoid hundreds of active pieces.

## Preserved generator prompt (from Blender/MODEL_FACTORY/TASKS/DL-006_CORAL_FAMILY.md, historical folder name; Blender is not used)

“Create a premium stylized underwater coral family for a colorful exploration game: five separate silhouettes including branching sea fan, rounded brain coral, layered plate coral, thick tubular coral and compact mound coral. Rich controlled coral pink, orange, violet, mint and turquoise accents; detailed organic ridges and polyps; beautiful readable forms against deep ocean water; artistically coherent species design; clean game-ready topology with fine detail baked where appropriate; UV-ready PBR; no rock base attached; no millions of polygons; no thin fragile tips. Each piece has a stable bottom pivot and can be combined into a modular reef.”

## Honest status
Actual model files committed: 0. Roblox Studio import/validation: NOT STARTED (intentionally deferred). No geometry statistics, licenses or tests are claimed.
