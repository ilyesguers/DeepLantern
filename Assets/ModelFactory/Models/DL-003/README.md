# DL-003 — Static dive / sonar beacon (visual prop)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1156 triangles, 7 materials, no textures) built from Python-authored geometry (`source/generate_dl003.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
A static, anchored landmark prop for existing MVP zones. No deployable network, GPS markers, passive rewards or new system; the emissive ring is only a visual accent.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).


## Measured size (metres, from the file)
2.367 (X) x 2.47 (Y) x 2.0499 (Z). Y up. Pivot: Bottom centre of the base (0,0,0); flat base on y=0.

## Notes
Teal pressure housing, titanium rings, six-rib protective cage with a thin cyan luminous ring, sensor head, side service ports, orange grab handles, tether eye and three deployed feet. Pivot at the base bottom centre so it sits flat on the seafloor.

## Limitations
Tether eye and service hatch are static geometry. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
