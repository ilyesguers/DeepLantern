# DL-015 — Cave entrance kit (mouth, ledge, buttress, accent)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1002 triangles, 12 materials, no textures) built from Python-authored geometry (`source/generate_dl015.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
A small secret/point of interest inside an existing MVP zone. No new zone, procedural caves, GPS marker or deferred Ruins content. The entrance is left open; the dark back wall is set back from the opening.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/rock_mouth.glb` — 416 tris, size [13.0473, 7.0822, 4.4694]
- `parts/overhanging_ledge.glb` — 114 tris, size [8.8313, 4.8, 4.8294]
- `parts/side_wall_buttress.glb` — 216 tris, size [4.5022, 3.3, 4.2636]
- `parts/mineral_accent.glb` — 256 tris, size [1.1064, 0.97, 0.906]

## Measured size (metres, from the file)
18.0383 (X) x 10.0 (Y) x 5.5972 (Z). Y up. Pivot: Each part in parts/ has its pivot at ground-contact centre (y=0), mouth facing +Z. model.glb shows an illustrative arrangement (ledge raised 5.1 m, buttress 9.5 m to -X), not a verified snap assembly.

## Notes
Pieces: rock mouth with arch, overhanging ledge with a thin luminous mineral seam, side-wall buttress, and a separate mineral accent cluster. model.glb shows an illustrative arrangement, not a verified snap assembly.

## Limitations
Only a finished-material preview exists (no neutral gray blockout). Interior is a shallow back wall, not a navigable tunnel. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
