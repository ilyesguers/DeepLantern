# DL-013 — BLOCKED

Asset: DL-013 — Discovery Specimen Display
Priority/GDD fit: MVP core support
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
Audit row for DL-013 (Discovery display):

Aquarium/Gallery display for mastered marine life and relics. Visual showcase only: no passive income or stat bonuses.

## Preserved generator prompt (from Blender/MODEL_FACTORY/TASKS/DL-013_DISCOVERY_DISPLAY.md, historical folder name; Blender is not used)

“Stylized premium underwater research specimen display pedestal: compact stable base, reinforced clear dome or protected window, replaceable specimen mount, thin cyan inspection ring, warm off-white casing, dark teal support and small blank label plate. Designed to make an unusual mineral or biological sample feel scientifically important, clean industrial construction, optimized game mesh, UV-ready PBR, no baked text or logos.”

## Honest status
Actual model files committed: 0. Roblox Studio import/validation: NOT STARTED (intentionally deferred). No geometry statistics, licenses or tests are claimed.
