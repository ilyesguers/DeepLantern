# DL-018 — Research equipment crates (hard case, supply crate + lid, instrument case)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (3,040 triangles, 6 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) built from Python-authored geometry (`source/generate_dl018.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Existing cargo/station dressing only. No inventory, dropper or storage mechanics.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/hard_case.glb` — 192 tris, size [0.82, 0.365, 0.6]
- `parts/supply_crate_body.glb` — 192 tris, size [1.44, 0.96, 1.06]
- `parts/supply_crate_lid.glb` — 72 tris, size [1.44, 0.195, 1.08]
- `parts/instrument_case.glb` — 216 tris, size [0.92, 0.405, 0.635]

## Measured size (metres, from the file)
4.17 (X) x 1.105 (Y) x 1.08 (Z). Y up. Pivot: Each part has its pivot at base centre (y=0); the lid's origin is its bottom centre. model.glb shows a hard case stacked on a second one to the left as a visual-clipping check (not a measured test).

## Notes
Hard case with handle and latches, large sealed supply crate with reinforced ribs and a separate lid object, and a fragile-instrument case with shock-isolating feet. Each has a blank label plate and a flat stable base.

## Limitations
Scuffing is not modelled (procedural detail textures only). The stacked arrangement in model.glb is a visual check, not a measured clipping test. Stylised first pass with v2 shading (baked vertex AO, smoothed normals, procedural grayscale detail textures; no hand-painted textures); Roblox import, scale fit, collision and mobile performance are not tested.
