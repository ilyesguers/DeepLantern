# DL-016 — Cable and hose kit (7 pieces)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1892 triangles, 7 materials, no textures) built from Python-authored geometry (`source/generate_dl016.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Static dressing only. No simulated cable physics, power network or interactive connection.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/hose_straight.glb` — 208 tris, size [3.12, 0.3808, 0.3808]
- `parts/hose_90_bend.glb` — 240 tris, size [1.6504, 0.3808, 2.2504]
- `parts/hose_u_bend.glb` — 288 tris, size [1.58, 0.3808, 1.5808]
- `parts/coiled_cable.glb` — 636 tris, size [1.2849, 1.056, 1.3669]
- `parts/wall_connector.glb` — 240 tris, size [0.5, 0.5, 0.37]
- `parts/pressure_coupling.glb` — 164 tris, size [1.0, 0.4311, 0.425]
- `parts/cable_clamp.glb` — 116 tris, size [0.4, 0.4, 0.34]

## Measured size (metres, from the file)
9.26 (X) x 1.056 (Y) x 7.3769 (Z). Y up. Pivot: Hose pieces: start attachment end at the origin, running toward +X (bend/U turn toward +Z), centreline 0.2 m above the floor plane. Wall connector: back plane z=0, socket faces +Z. model.glb spaces the pieces for preview.

## Notes
Hose radius 0.12 m with 0.17 m connectors on every end (strain-relief bands in amber). Pieces: straight, 90-degree bend, U-bend, coiled cable, wall connector, pressure coupling, cable clamp. No loose ends: every hose end has a connector. Hose start end is the pivot.

## Limitations
Hoses are faceted 8-sided sweeps; the coil is dark and low-contrast against dark water. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
