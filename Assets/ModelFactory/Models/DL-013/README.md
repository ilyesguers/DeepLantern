# DL-013 — Discovery specimen display (pedestal + replaceable specimen)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (614 triangles, 8 materials, no textures) built from Python-authored geometry (`source/generate_dl013.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Visual showcase for the Aquarium/Gallery wing. No passive income, stat bonus or interaction. The specimen is a separate replaceable object and the label plate is blank for in-game UI.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/display_pedestal.glb` — 502 tris, size [1.24, 1.73, 1.24]
- `parts/specimen_placeholder.glb` — 112 tris, size [0.22, 0.4263, 0.22]

## Measured size (metres, from the file)
1.24 (X) x 1.73 (Y) x 1.24 (Z). Y up. Pivot: Pedestal: floor centre (0,0,0). Specimen placeholder: bottom centre; model.glb seats it on the mount at y=1.03.

## Notes
Octagonal pedestal with a single thick glass dome (no overlapping transparent shells), a thin cyan inspection ring, specimen mount and blank label plate. parts/specimen_placeholder.glb is a simple violet crystal stand-in; model.glb seats it on the mount.

## Limitations
Dome uses alpha blending; check it on mobile or substitute a Studio glass material. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
