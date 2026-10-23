# DL-019 — BLOCKED

Asset: DL-019 — Small Underwater Fauna Family
Priority/GDD fit: MVP-compatible, later in asset queue
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
Audit row for DL-019 (Small fauna):

Non-lethal Codex creatures using light shared/simple rigs when actually needed. No creature capture inventory, predator/prey ecosystem, complex AI, or combat. If only a static mesh is available, label it unrigged; do not claim animation.

## Preserved generator prompt (from Blender/MODEL_FACTORY/TASKS/DL-019_SMALL_FAUNA.md, historical folder name; Blender is not used)

“Three charming premium stylized small underwater creatures for an exploration game: colorful tiny reef fish, graceful jellyfish with a luminous bell and thick readable tentacles, and a small shrimp-like cleaner creature. Friendly and scientifically curious, not cartoonishly flat and not horror. Beautiful clean silhouettes, controlled saturated colors, subtle material variation, optimized game-ready topology, no swarms, no thin invisible tendrils, UV-ready PBR. Keep major anatomical parts sensibly separated for possible later rigging.”

## Honest status
Actual model files committed: 0. Roblox Studio import/validation: NOT STARTED (intentionally deferred). No geometry statistics, licenses or tests are claimed.
