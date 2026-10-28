# DL-014 — Submarine docking pad + service arm (compact Docking Ring-compatible)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (2,388 triangles, 6 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) built from Python-authored geometry (`source/generate_dl014.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Every figure below was measured from the exported files.

## GDD scope
Visual props that fit the existing Sub Dock and the compact MVP Docking Ring. No public matchmaking, crowd/social plaza, launch mechanics or replacement of the functional pad without Studio review. The arm is a static mesh (not animated).

## Files
`model.glb` (primary), `model.obj` + `model.mtl`, `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry), `source/` (editable generator).
Per-part files:
- `parts/pad.glb` — 396 tris, size [6.4, 1.8026, 10.45]
- `parts/arm.glb` — 488 tris, size [3.4299, 2.3985, 1.4]

## Measured size (metres, from the file)
8.6 (X) x 2.3985 (Y) x 10.45 (Z). Y up. Pivot: parts/pad.glb: centre of the floor-contact plane (0,0,0). parts/arm.glb: foot centre on the floor. model.glb places the arm 4.7 m to the -X side of the pad.

## Notes
parts/pad.glb: platform with raised anti-slip inset panels, four guide marks, centre line, two V-cradle supports (spacing matches the DL-001 skids at x=+/-1.15), corner maintenance light posts and front status indicators. parts/arm.glb: swivel pylon, two-segment articulated-looking arm, coupler ring and static hose. model.glb places the arm 4.7 m to the -X side of the pad. Floor-contact plane is flat at y=0.

## Limitations
Arm is unrigged; hose is a chain of static boxes; cradle clearance against the real submarine not tested in Studio. Stylised first pass with v2 shading (baked vertex AO, smoothed normals, procedural grayscale detail textures; no hand-painted textures); Roblox import, scale fit, collision and mobile performance are not tested.
