# DL-012 — Ancient seafloor relic (clean + partly buried)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1640 triangles, 11 materials, no textures) built from Python-authored geometry (`source/generate_dl012.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
A discoverable prop for existing Relics, Codex and Archive categories. No new lore, zone or mechanic; a full Lost Ruins area is post-MVP. No runes are modelled.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/relic_clean.glb` — 760 tris, size [9.5, 9.5, 1.75]
- `parts/relic_buried.glb` — 880 tris, size [11.6453, 9.5, 5.2277]

## Measured size (metres, from the file)
22.3452 (X) x 10.7 (Y) x 5.2277 (Z). Y up. Pivot: Base centre (0,0,0) for each part; ring faces +Z. model.glb shows clean (x=-6) and buried (x=+6) side by side.

## Notes
Broken concentric rings, a sealed aperture disc with a cyan glow ring and three seams, two support pylons and a base block. parts/relic_clean.glb is the clean version; parts/relic_buried.glb is sunk 1.2 m into a sediment mound for terrain blending.

## Limitations
Rings are faceted from 24 and 18 box segments; fine detail must come from material masks later. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
