# DL-011 — Twilight Reef landmark arch

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1,210 triangles, 9 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) built from Python-authored geometry (`source/generate_dl011.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
One readable landmark within the existing Twilight Reef zone (Zone_TwilightReef); not a new zone or traversal mechanic. The opening is clear (about 6 m wide).

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).


## Measured size (metres, from the file)
14.7133 (X) x 8.796 (Y) x 4.9974 (Z). Y up. Pivot: Centre of the footprint on the seafloor (0,0,0); opening faces +/-Z, spans X.

## Notes
Asymmetric blue and warm-stone supports, a curved lintel, coral shelves and four luminous focal growths. Triangle count is below the 8k-18k target in the brief; it is a mobile-friendly mid-poly landmark.

## Limitations
No baked detail maps; coral shelves are simple lumps. Not checked against actual Twilight Reef terrain. Stylised first pass with v2 shading (baked vertex AO, smoothed normals, procedural grayscale detail textures; no hand-painted textures); Roblox import, scale fit, collision and mobile performance are not tested.
