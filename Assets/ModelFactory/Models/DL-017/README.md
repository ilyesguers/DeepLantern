# DL-017 — Navigation signage kit (5 blank plates)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (624 triangles, 6 materials, no textures) built from Python-authored geometry (`source/generate_dl017.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Diegetic wayfinding only. No GPS quest markers, minimap or UI system. Plates are blank so text and arrows can come from Roblox UI or decals; the cyan chevrons are geometric marks, not words.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/wall_plaque.glb` — 120 tris, size [1.2, 0.6, 0.135]
- `parts/hanging_directional.glb` — 108 tris, size [1.85, 1.11, 0.16]
- `parts/floor_route_marker.glb` — 120 tris, size [1.0, 0.085, 1.0]
- `parts/hazard_panel.glb` — 156 tris, size [1.4, 0.8, 0.125]
- `parts/equipment_plate.glb` — 120 tris, size [0.45, 0.28, 0.1]

## Measured size (metres, from the file)
8.125 (X) x 2.26 (Y) x 1.0 (Z). Y up. Pivot: Wall pieces: back plane z=0, bottom centre, facing +Z. Hanging sign: ceiling attachment at the origin. Floor marker: centre of floor contact.

## Notes
Pieces: wall plaque, hanging directional sign, floor route marker, hazard stripe panel, numbered-equipment plate (blank). Wall pieces face +Z with the back plane at z=0.

## Limitations
No preview with placeholder glyphs was produced (the brief asked for one); only blank production plates are shown. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
