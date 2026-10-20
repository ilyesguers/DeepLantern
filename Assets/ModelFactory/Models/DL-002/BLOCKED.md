# DL-002 — BLOCKED

Asset: DL-002 — Modular Research Station Kit
Priority/GDD fit: MVP core
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
Audit row for DL-002 (Research station kit):

Only Outpost, Station, Complex and the documented MVP wings: Power Core, Sub Dock, Workshop, Research Lab, Aquarium/Gallery, Archive, Observatory. Modular reuse; no Citadel/Deep Empire or massive hub.

## GDD-aligned task brief (Assets/ModelFactory/Tasks/DL-002.md)

Visual / generation brief:

> premium modular compact underwater science station kit, consistent snap dimensions and connector language, dark navy structure, off-white panels, restrained teal glass and orange safety markings, clean purposeful industrial design, reusable parts, Roblox optimized low-poly export, no text-dependent gameplay

GDD-aligned generator prompt:

> premium modular compact underwater science station kit, consistent snap dimensions and connector language, dark navy structure, off-white panels, restrained teal glass and orange safety markings, clean purposeful industrial design, reusable parts, Roblox optimized low-poly export, no text-dependent gameplay. Produce a real downloadable 3D model/export, not merely a 2D concept image. If the available tool cannot generate actual 3D files, mark this task BLOCKED and describe the missing capability; do not fake deliverables.

## Preserved generator prompt (from Blender/MODEL_FACTORY/TASKS/DL-002_RESEARCH_STATION_KIT.md, historical folder name; Blender is not used)

“Professional modular underwater research station architecture kit for a stylized premium exploration game. Create separate snap-fit modular pieces: pressure-rated wall, reinforced window wall, corner wall, floor tile, ceiling rib, sealed hatch door, railing, cable tray, pipe bundle, floodlight bracket and ventilation/filter unit. Consistent modular grid, engineered proportions, thick readable forms, off-white enamel panels, deep blue structural frame, orange safety handles, restrained cyan indicator lights, subtle marine wear. Clean topology, UV-ready, game-optimized, no text, no logos, no floating pieces. Each part has a deliberate origin/pivot and must assemble seamlessly with matching dimensions.”

## Honest status
Actual model files committed: 0. Roblox Studio import/validation: NOT STARTED (intentionally deferred). No geometry statistics, licenses or tests are claimed.
