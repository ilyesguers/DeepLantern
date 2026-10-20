# DL-015 — BLOCKED

Asset: DL-015 — Underwater Cave Entrance Kit
Priority/GDD fit: MVP-compatible, conditional
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
Audit row for DL-015 (Cave entrance kit):

A small secret/point of interest inside an existing MVP zone. No new zone, procedural cave generation, GPS marker, or deferred advanced Ruins content.

## Preserved generator prompt (from Blender/MODEL_FACTORY/TASKS/DL-015_CAVE_ENTRANCE.md, historical folder name; Blender is not used)

“Stylized underwater cave entrance modular kit: broad sculpted rock mouth with clear passage, overhanging ledge, side-wall buttress and optional small mineral-coral accent. Layered erosion, rounded edges, subtle teal/cyan mineral veins and sparse coral, dramatic but inviting atmosphere, no horror-mouth silhouette, no obstructing geometry, optimized game-ready mesh, UV-ready PBR, modular separate pieces with documented bounds.”

## Honest status
Actual model files committed: 0. Roblox Studio import/validation: NOT STARTED (intentionally deferred). No geometry statistics, licenses or tests are claimed.
