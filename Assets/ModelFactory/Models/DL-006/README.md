# DL-006 — Coral family (5 species)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (2,776 triangles, 7 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) built from Python-authored geometry (`source/generate_dl006.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Static dressing for Shallows and Twilight Reef only. Reusable silhouettes, low object count; no ecosystem simulation.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/branching_fan.glb` — 634 tris, size [2.0605, 2.1111, 0.7704]
- `parts/brain_coral.glb` — 564 tris, size [1.5952, 1.28, 1.609]
- `parts/plate_coral.glb` — 160 tris, size [1.9958, 1.2284, 2.1077]
- `parts/tubular_coral.glb` — 876 tris, size [1.5079, 1.635, 1.4134]
- `parts/mound_coral.glb` — 542 tris, size [1.3244, 1.0, 1.2153]

## Measured size (metres, from the file)
11.3636 (X) x 2.1111 (Y) x 2.1077 (Z). Y up. Pivot: Each part in parts/ has its pivot at seafloor contact (base centre, y=0). model.glb lays the five out 2.4 m apart along X.

## Notes
Species: branching sea fan, brain coral, plate coral, tubular coral, mound coral with polyps. Colour varies by species (pink, mint/turquoise, violet, orange). Each is a separate part under parts/ with its pivot at seafloor contact; model.glb lays them out 2.4 m apart.

## Limitations
Fine pores/ridges are not modelled and there are no scale variants. Stylised first pass with v2 shading (baked vertex AO, smoothed normals, procedural grayscale detail textures; no hand-painted textures); Roblox import, scale fit, collision and mobile performance are not tested.
