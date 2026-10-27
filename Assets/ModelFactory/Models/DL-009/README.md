# DL-009 — Bioluminescent flora (3 assets)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (1618 triangles, 11 materials, no textures) built from Python-authored geometry (`source/generate_dl009.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Existing MVP-zone dressing and discovery visuals. No bloom/event logic, particles or gameplay. Emissive parts are limited to small rims, cores and tips.

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/cup_anemone.glb` — 468 tris, size [1.32, 1.51, 1.3948]
- `parts/bulb_cluster.glb` — 898 tris, size [1.438, 2.036, 1.4003]
- `parts/glowing_sea_flower.glb` — 252 tris, size [1.0769, 2.2013, 1.0263]

## Measured size (metres, from the file)
5.6423 (X) x 2.2213 (Y) x 1.4673 (Z). Y up. Pivot: Each part in parts/ has its pivot at base centre (y=0). model.glb spaces the three 2.2 m apart along X.

## Notes
Cup anemone (glowing rim and core), bulb cluster (violet stalks with teal/violet/amber bulb tips) and a thin-stemmed sea flower. Bodies are non-emissive; glow is on separate meshes so it can be tuned or recoloured in Studio.

## Limitations
The flower stem is a 0.05 m-radius sweep that may be thin at distance. Stylised first pass with flat materials and no UV/texture detail; Roblox import, scale fit, collision and mobile performance are not tested.
