# DL-004 — BLOCKED

Asset: DL-004 — Sample Canister Family
Priority/GDD fit: MVP-compatible
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
Audit row for DL-004 (Sample canister family):

Biological samples / field consumables and existing cargo/debrief flow only. No new inventory type, currencies, crafting or capture mechanics.

## Preserved generator prompt (from Blender/MODEL_FACTORY/TASKS/DL-004_SAMPLE_CANISTERS.md, historical folder name; Blender is not used)

“Professional stylized scientific underwater specimen canister set, three coherent variants: cylindrical standard pressure capsule with protected clear chamber and metal end caps; caged biological sample container with replaceable visible specimen; compact hexagonal rare-mineral vault with reinforced window. Deep teal/navy housing, off-white labels, orange locking clamps, cyan and violet scientific status lights, believable pressure seals, handles and recessed seams. Premium authored game-asset quality, readable silhouettes, optimized clean topology, UV-ready PBR, no text/logo, no thin fragile pieces. Export each variant separately and as one preview collection.”

## Honest status
Actual model files committed: 0. Roblox Studio import/validation: NOT STARTED (intentionally deferred). No geometry statistics, licenses or tests are claimed.
