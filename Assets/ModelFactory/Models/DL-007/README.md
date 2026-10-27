# DL-007 — Kelp cluster (small, medium, tall)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (3270 triangles, 10 materials, no textures) built from Python-authored geometry (`source/generate_dl007.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Kelp Forest dressing only; no ecosystem simulation or growth logic.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/kelp_small.glb` — 814 tris, size [1.0361, 2.4795, 1.0165]
- `parts/kelp_medium.glb` — 1106 tris, size [1.2319, 4.0209, 1.2278]
- `parts/kelp_tall.glb` — 1350 tris, size [1.775, 6.0458, 1.4347]

## Measured size (metres, from the file)
5.0474 (X) x 6.0458 (Y) x 1.4347 (Z). Y up. Pivot: Each part in parts/ has its pivot at the root centre on the seafloor (y=0). model.glb lays the three out 1.8 m apart along X.

## Notes
Each cluster has a rock root, curved tapering ribbon fronds in three green tones, thicker stipes and a few gold gas bladders. Small 5 fronds, medium 7, tall 9. No sway animation is included; fronds are static meshes.

## Limitations
Fronds are single thin ribbons (thickness 0.05 m), which may look sparse when seen edge-on; no translucency. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
