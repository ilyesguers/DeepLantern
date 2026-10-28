# DL-002 — MVP modular research station kit (14 modules)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (6,036 triangles, 9 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) built from Python-authored geometry (`source/generate_dl002.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Restricted to the GDD MVP tiers Outpost -> Station -> Complex and the named MVP wings. Reusable architectural modules only; no Citadel/Deep Empire, giant hub, grid-building system, droppers or passive generators.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/wall_panel.glb` — 72 tris, size [4.0, 3.0, 0.5]
- `parts/window_wall.glb` — 156 tris, size [4.0, 3.0, 0.5]
- `parts/corner_wall.glb` — 168 tris, size [4.23, 3.0, 4.05]
- `parts/door_frame.glb` — 168 tris, size [4.0, 3.0, 0.52]
- `parts/hatch.glb` — 468 tris, size [4.0, 3.0, 0.61]
- `parts/service_access_panel.glb` — 144 tris, size [4.0, 3.0, 0.51]
- `parts/floor_tile.glb` — 108 tris, size [4.0, 0.325, 4.0]
- `parts/ceiling_beam.glb` — 48 tris, size [4.0, 0.48, 0.6]
- `parts/railing_short.glb` — 72 tris, size [2.115, 1.07, 0.14]
- `parts/railing_corner.glb` — 144 tris, size [1.715, 1.07, 1.715]
- `parts/pipe_bundle.glb` — 156 tris, size [4.0, 0.75, 0.565]
- `parts/cable_tray.glb` — 168 tris, size [4.0, 0.34, 0.62]
- `parts/floodlight_bracket.glb` — 132 tris, size [0.5, 0.77, 1.084]
- `parts/vent_filter_unit.glb` — 160 tris, size [1.32, 0.8, 0.61]

## Measured size (metres, from the file)
20.5 (X) x 3.07 (Y) x 15.094 (Z). Y up. Pivot: Grid unit 4.0 m wide, 3.0 m tall, 0.4 m wall. Wall-type modules: origin at bottom centre of the wall line. model.glb is a spaced preview layout of the 14 modules, not an assembly; use parts/*.glb.

## Notes
Grid unit: 4.0 m wide x 3.0 m tall x 0.4 m wall thickness. Modules (each also in parts/): wall_panel, window_wall, corner_wall, door_frame (pressure seal, no door leaf), hatch (wheel + lock lugs), service_access_panel, floor_tile (service channel), ceiling_beam, railing_short, railing_corner, pipe_bundle, cable_tray, floodlight_bracket, vent_filter_unit. Wall-type origins are at the bottom centre of the wall line. model.glb is a spaced preview layout, not a snapped assembly. No snap test or 3x2 assembly check has been run in Studio.

## Limitations
Door frame has no door leaf; hatch wheel is static; corner wall is a single L piece. Stylised first pass with v2 shading (baked vertex AO, smoothed normals, procedural grayscale detail textures; no hand-painted textures); Roblox import, scale fit, collision and mobile performance are not tested.
