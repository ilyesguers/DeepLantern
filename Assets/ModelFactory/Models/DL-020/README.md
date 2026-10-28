# DL-020 — Lighting fixture kit (work lamp, wall floodlight, nav beacon)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1044 triangles, 8 materials, no textures) built from Python-authored geometry (`source/generate_dl020.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Fixture meshes only. No Roblox light objects, scripts or shadow settings; actual SpotLight/SurfaceLight setup is a later Studio step.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/work_lamp.glb` — 424 tris, size [0.8368, 1.5356, 0.6813]
- `parts/wall_floodlight.glb` — 360 tris, size [0.533, 0.6532, 0.7663]
- `parts/nav_beacon.glb` — 260 tris, size [0.64, 0.765, 0.6393]

## Measured size (metres, from the file)
3.6318 (X) x 1.5356 (Y) x 1.1033 (Z). Y up. Pivot: Work lamp: clamp base centre (y=0). Floodlight: back plane z=0, faces +Z. Nav beacon: base centre (y=0). No light objects included.

## Notes
Adjustable work lamp, wall floodlight with heat-vent fins and guard bars, and a compact cyan navigation beacon. Lens glow is a restrained emissive material that does not replace geometry.

## Limitations
The work lamp arm is a fixed pose, not articulated. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
