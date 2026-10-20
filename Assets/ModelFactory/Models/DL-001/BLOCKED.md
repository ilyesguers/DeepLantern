# DL-001 — BLOCKED

Asset: DL-001 — Deep-Diving Research Submarine
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
Audit row for DL-001 (Research submarine):

Visual asset for the existing MVP Scout / submarine workflow. Do not introduce another playable class, new controls, or altered stats. Preserve existing gameplay model/contracts; replacement/integration happens later in Studio.

## GDD-aligned task brief (Assets/ModelFactory/Tasks/DL-001.md)

Visual / generation brief:

> premium stylized compact research submarine, Roblox-ready low-poly clean topology, strong silhouette, deep navy/graphite hull, off-white enamel, restrained safety orange and cyan lenses, no weapons, no excessive microdetail, orthographic 3/4 studio render and real export

GDD-aligned generator prompt:

> premium stylized compact research submarine, Roblox-ready low-poly clean topology, strong silhouette, deep navy/graphite hull, off-white enamel, restrained safety orange and cyan lenses, no weapons, no excessive microdetail, orthographic 3/4 studio render and real export. Produce a real downloadable 3D model/export, not merely a 2D concept image. If the available tool cannot generate actual 3D files, mark this task BLOCKED and describe the missing capability; do not fake deliverables.

## Preserved generator prompt (from Blender/MODEL_FACTORY/TASKS/DL-001_RESEARCH_SUBMARINE.md, historical folder name; Blender is not used)

“Create a polished, game-ready stylized deep-sea research submarine for a premium Roblox underwater exploration adventure. Compact elongated pressure hull, protected large forward observation dome with thick metal rim, paired guarded rear thrusters, small cyan sensor lights, practical side buoyancy housings, top sonar mast and access hatch, service panels, restrained orange safety markings, navy graphite and warm off-white materials. Authored professional silhouette, layered primary/secondary/tertiary forms, clean readable topology, realistic engineering logic, no weapons, no text logos, no floating details, no thin fragile parts. Designed for real-time third-person gameplay, optimized low-to-mid poly, baked detail where possible, clean UVs, PBR materials. Produce a coherent single asset with consistent scale and a centered vehicle-root pivot.”

## Honest status
Actual model files committed: 0. Roblox Studio import/validation: NOT STARTED (intentionally deferred). No geometry statistics, licenses or tests are claimed.
