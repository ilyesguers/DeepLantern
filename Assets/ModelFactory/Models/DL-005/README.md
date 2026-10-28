# DL-005 — Research Lab console (visual prop)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1,524 triangles, 6 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) built from Python-authored geometry (`source/generate_dl005.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Visual prop for the existing Research Lab terminal. No new terminal feature, UI, scripts or API; screens are plain emissive panels (no baked text or interface graphics).

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).


## Measured size (metres, from the file)
1.3 (X) x 1.685 (Y) x 0.775 (Z). Y up. Pivot: Floor centre of the base (0,0,0); user side is +Z.

## Notes
Weighted base and cabinet, angled main screen and secondary status panel, three guarded switches, three rotary selectors, four push buttons, scanner pad with a thin cyan ring, cable conduit to a floor connector, vents, access panel and a two-light lamp bar. User side is +Z.

## Limitations
Screens and scanner ring are single emissive meshes; no separate animated parts. Stylised first pass with v2 shading (baked vertex AO, smoothed normals, procedural grayscale detail textures; no hand-painted textures); Roblox import, scale fit, collision and mobile performance are not tested.
