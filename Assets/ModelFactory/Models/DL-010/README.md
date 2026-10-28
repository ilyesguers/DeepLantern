# DL-010 — Small wreckage set (6 pieces)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1,792 triangles, 5 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) built from Python-authored geometry (`source/generate_dl010.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Small static points of interest within an existing MVP zone; not a wreck-dungeon, structural simulation or combat system. Faded research blue, dark metal, a few orange remnants; no gore or horror shapes.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/bent_panel.glb` — 72 tris, size [2.5, 0.8947, 2.3215]
- `parts/broken_support_frame.glb` — 72 tris, size [2.7186, 2.4734, 1.0237]
- `parts/sensor_housing.glb` — 264 tris, size [1.1765, 1.77, 1.1449]
- `parts/cracked_pressure_door.glb` — 324 tris, size [2.7427, 2.3024, 1.3029]
- `parts/pipe_segment.glb` — 252 tris, size [2.4584, 0.7228, 0.9829]
- `parts/damaged_crate.glb` — 168 tris, size [1.781, 1.1242, 1.4265]

## Measured size (metres, from the file)
18.1549 (X) x 2.5274 (Y) x 2.3215 (Z). Y up. Pivot: Each part in parts/ has its pivot at ground contact (y=0). model.glb spaces the six along X.

## Notes
Pieces: bent panel, broken support frame, sensor housing with snapped mast, cracked pressure door, pipe segment with jagged end, damaged crate. Damage is in the geometry (bends, breaks, tilted caps).

## Limitations
Cracks are modelled as gaps/offset pieces, not fine fracture lines; no decals or grime textures. Stylised first pass with v2 shading (baked vertex AO, smoothed normals, procedural grayscale detail textures; no hand-painted textures); Roblox import, scale fit, collision and mobile performance are not tested.
