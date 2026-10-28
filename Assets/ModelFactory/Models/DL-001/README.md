# DL-001 — Scout / research submarine (visual asset)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (6,254 triangles, 9 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) of the Scout submarine, built from Python-authored geometry (`source/generate_dl001.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Proportions and colours follow `Art/VisualReference/02_Submarine_Design.png`: white hull, graphite/navy structure, amber accents, cyan glass and glow.

## GDD scope
Visual only, for the existing MVP Scout. No new class, controls, stats, weapons or crew mechanics. Gameplay model, controller contracts and mounting points are untouched; replacing the live visual happens later in Studio after review.

## Files
- `model.glb` (primary), `model.obj` + `model.mtl` (same geometry), `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry: 3/4, side, front, top), `source/generate_dl001.py` (editable source).

## Parts (one mesh per material = one MeshPart each)
`hull_offwhite`, `graphite_navy` (bands, keel, skids, pods, thrusters, fins, mast), `amber_accent`, `glass_cyan` (cockpit dome, alpha 0.5), `emissive_cyan` (nose lantern, work lights, thruster glow, porthole, mast tip).

## Measured size (from the file)
Whole file incl. static FX light-beam meshes: 4.28 (W) x 3.85 (H) x 15.69 (L) metres (bounds z -9.79..5.9). The hull itself is about 8.5 m long; the extra length is the translucent fx_beam_cyan nose-lantern beam (68 triangles, optional - delete the fx_* meshes if not wanted). The design sheet gives 8 x ~4.2 x 3.1 m, so the hull is slightly larger. Scale to match the existing submarine in Studio.

## Orientation / pivot
Y up, nose toward -Z, +X right. Origin at hull centreline mid-length. Not verified against how Roblox imports glTF.

## Import and performance notes (not yet tested)
Import via Studio 3D Importer; 9 MeshParts (one per material, incl. 2 optional fx_* translucent meshes). Use a simplified collision shape, not per-triangle fidelity. Glass uses alpha blending; check it renders acceptably on mobile or swap to a Studio Glass material. Emissive parts are meant to be recoloured with Neon/lights in Studio.

## Limitations
Stylised first pass: smooth capsule hull, no UV/texture detail, no moving parts (thrusters/hatch are not separate), no wear. Side pods are partly hidden by the hull in the side view.
