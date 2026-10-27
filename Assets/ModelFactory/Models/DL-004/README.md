# DL-004 — Sample canister family (3 variants)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (984 triangles, 8 materials, no textures) built from Python-authored geometry (`source/generate_dl004.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Visual props for the existing biological-sample / cargo / debrief categories. No new inventory type, crafting or capture mechanic. Sample contents are separate meshes so they can be swapped; label plates are empty (no baked text).

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/standard_capsule.glb` — 356 tris, size [0.44, 0.71, 0.455]
- `parts/fragile_bio_sample.glb` — 448 tris, size [0.4, 0.605, 0.45]
- `parts/mineral_vault.glb` — 180 tris, size [0.59, 0.47, 0.56]

## Measured size (metres, from the file)
2.115 (X) x 0.71 (Y) x 0.56 (Z). Y up. Pivot: Each variant in parts/ has its origin at its geometric centre; model.glb places the three side by side at x=-0.8/0/+0.8 with bottoms on y=0.

## Notes
Three variants share one palette and scale family: standard pressure capsule, caged fragile biological sample (violet content), and a hexagonal rare-mineral vault with a reinforced window. model.glb places all three side by side; each variant is also exported on its own under parts/.

## Limitations
Glass uses alpha blending; silhouettes and colour bands still identify each variant if transparency renders poorly. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
