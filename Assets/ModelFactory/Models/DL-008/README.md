# DL-008 — Seafloor rock kit (6 pieces)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1486 triangles, 9 materials, no textures) built from Python-authored geometry (`source/generate_dl008.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Reusable static geological dressing in approved zones; no terrain generation or destructible-terrain system.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/boulder.glb` — 220 tris, size [2.9965, 1.7, 2.6499]
- `parts/fractured_slab.glb` — 78 tris, size [3.7435, 2.6872, 2.0508]
- `parts/tall_split_rock.glb` — 124 tris, size [3.2035, 4.0, 1.7501]
- `parts/porous_volcanic.glb` — 586 tris, size [2.6034, 1.6, 2.0271]
- `parts/layered_shelf.glb` — 128 tris, size [3.1652, 1.6, 2.0845]
- `parts/scatter_cluster.glb` — 350 tris, size [1.8369, 0.63, 1.5449]

## Measured size (metres, from the file)
22.287 (X) x 4.4072 (Y) x 2.6499 (Z). Y up. Pivot: Each part in parts/ has its pivot at ground contact (base centre, y=0). model.glb spaces the six along X.

## Notes
Pieces: low boulder, fractured slab, tall split rock, porous volcanic stone, layered sediment shelf, scatter cluster. Two stone families: cool blue-grey and warm mineral. Each part has ground-contact pivot at y=0.

## Limitations
No normal-map or strata detail; bottoms are closed (not stripped). No seam-overlap composition test beyond the spaced layout. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
