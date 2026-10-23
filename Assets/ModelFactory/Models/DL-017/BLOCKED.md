# DL-017 — BLOCKED

Asset: DL-017 — Navigation Signage Kit
Priority/GDD fit: MVP support
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
Audit row for DL-017 (Signage kit):

Physical wayfinding and diegetic labels only. No quest-marker GPS, minimap, or new UI systems. Use concise readable text; do not bake unsupported language-specific gameplay text into meshes.

## Preserved generator prompt (from Blender/MODEL_FACTORY/TASKS/DL-017_SIGNAGE_KIT.md, historical folder name; Blender is not used)

“Modular stylized underwater research station signage kit with blank replaceable plates: wall plaque, hanging directional sign, floor route marker, hazard stripe panel and equipment ID plate. Thick navy frame, warm off-white face, orange safety accents and simple cyan navigation icon areas. Clear silhouette and high contrast at distance, no baked text or logos, low-poly optimized geometry, clean pivots for wall/floor mounting.”

## Honest status
Actual model files committed: 0. Roblox Studio import/validation: NOT STARTED (intentionally deferred). No geometry statistics, licenses or tests are claimed.
