# DL-019 — Small non-threatening fauna (reef fish, jellyfish, cleaner shrimp) - static, unrigged

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1816 triangles, 11 materials, no textures) built from Python-authored geometry (`source/generate_dl019.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Non-lethal Codex creatures. No capture inventory, ecosystem, AI, combat or animation. These are STATIC, UNRIGGED meshes; no skeleton or animation exists.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/reef_fish.glb` — 372 tris, size [0.42, 0.58, 0.9561]
- `parts/jellyfish.glb` — 700 tris, size [1.08, 1.3877, 1.08]
- `parts/cleaner_shrimp.glb` — 744 tris, size [0.6284, 0.4059, 1.4094]

## Measured size (metres, from the file)
3.4234 (X) x 1.3877 (Y) x 1.4094 (Z). Y up. Pivot: Creature visual centre; facing +Z. UNRIGGED static meshes (no skeleton, no animation). model.glb spaces the three along X.

## Notes
Fish body and fins use different materials so they import as separate MeshParts for later rigging; the jellyfish has a bell, glowing rim and eight thick tentacles; the shrimp has clear head, body and tail segmentation. No sharp teeth or horror features.

## Limitations
Not rigged. Creature scale is approximate (fish about 1 m long including tail). Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
