# DL-001 — Scout / research submarine (visual asset)

Status: UPLOADED_TO_GITHUB. Roblox Studio import/visual/performance: NOT TESTED (deferred by design).

## What this is
A real low-poly 3D model (2,032 triangles, 5 materials, no textures) of the Scout submarine, built from Python-authored geometry (`source/generate_dl001.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Proportions and colours follow `Art/VisualReference/02_Submarine_Design.png`: white hull, graphite/navy structure, amber accents, cyan glass and glow.

## GDD scope
Visual only, for the existing MVP Scout. No new class, controls, stats, weapons or crew mechanics. Gameplay model, controller contracts and mounting points are untouched; replacing the live visual happens later in Studio after review.

## Files
- `model.glb` (primary), `model.obj` + `model.mtl` (same geometry), `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry: 3/4, side, front, top), `source/generate_dl001.py` (editable source).

## Parts (one mesh per material = one MeshPart each)
`hull_offwhite`, `graphite_navy` (bands, keel, skids, pods, thrusters, fins, mast), `amber_accent`, `glass_cyan` (cockpit dome, alpha 0.5), `emissive_cyan` (nose lantern, work lights, thruster glow, porthole, mast tip).

## Measured size (from the file)
8.53 (L) x 4.28 (W) x 3.76 (H) metres including skids and sonar mast; the design sheet gives 8 x ~4.2 x 3.1 m, so this is slightly larger. Scale to match the existing submarine in Studio.

## Orientation / pivot
Y up, nose toward -Z, +X right. Origin at hull centreline mid-length. Not verified against how Roblox imports glTF.

## Import and performance notes (not yet tested)
Import via Studio 3D Importer; 5 MeshParts. Use a simplified collision shape, not per-triangle fidelity. Glass uses alpha blending; check it renders acceptably on mobile or swap to a Studio Glass material. Emissive parts are meant to be recoloured with Neon/lights in Studio.

## Limitations
Stylised first pass: smooth capsule hull, no UV/texture detail, no moving parts (thrusters/hatch are not separate), no wear. Side pods are partly hidden by the hull in the side view.
