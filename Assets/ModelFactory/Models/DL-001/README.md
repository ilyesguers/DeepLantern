# DL-001 — Scout / research submarine (visual asset)

Status: NEEDS_REVIEW. The v2 export passes the documented file-level re-read; this session independently parsed the GLB and compared its genuine software preview to v1. Roblox Studio import, fit, collision, lighting, controller alignment and performance: NOT TESTED.

## What this is
A real low-poly 3D model (6,254 triangles, 9 materials, v2 quality pass: chamfers, baked AO, smoothed normals, procedural detail textures) of the Scout submarine, built from Python-authored geometry (`source/generate_dl001.py` + `../../Tools/dlmesh.py`). It is not AI-generated and not sculpted in Blender. Proportions and colours follow `Art/VisualReference/02_Submarine_Design.png`: white hull, graphite/navy structure, amber accents, cyan glass and glow.

## GDD scope
Visual only, for the existing MVP Scout. No new class, controls, stats, weapons or crew mechanics. Gameplay model, controller contracts and mounting points are untouched; replacing the live visual happens later in Studio after review.

## Files
- `model.glb` (primary), `model.obj` + `model.mtl`, `textures/` (two embedded 256 px detail maps), `manifest.json` (measured numbers + SHA-256), `preview.png` (software render of the exported geometry: 3/4, side, front, top), `source/generate_dl001.py` (editable source).

## Parts (one mesh per material = one MeshPart each)
The v2 GLB has nine material meshes: `hull_offwhite`, `graphite_navy`, `amber_accent`, `titanium_t`, `glass_cyan`, `emissive_cyan`, `emissive_amber`, `fx_beam_cyan` and `fx_halo_cyan`. Cockpit glass is alpha 0.5. The FX meshes are static geometry, not Roblox lights or particles.

## Measured size (from the file)
Whole file incl. static FX light-beam meshes: 4.28 (W) x 3.85 (H) x 15.69 (L) metres (bounds z -9.79..5.9). The hull itself is about 8.5 m long; the extra length is the translucent fx_beam_cyan nose-lantern beam (68 triangles, optional - delete the fx_* meshes if not wanted). The design sheet gives 8 x ~4.2 x 3.1 m. Do not scale the whole export to hide the beam or height mismatch; correct the hull and optional FX separately.

## Orientation / pivot
Y up, nose toward -Z, +X right. Origin at hull centreline mid-length. Not verified against how Roblox imports glTF.

## Import and performance notes (not yet tested)
Import via Studio 3D Importer; 9 MeshParts (one per material, incl. 2 optional fx_* translucent meshes). Use a simplified collision shape, not per-triangle fidelity. Glass uses alpha blending; check it renders acceptably on mobile or swap to a Studio Glass material. Emissive parts are meant to be recoloured with Neon/lights in Studio.

## Current review findings (2026-10-27)
- The v2 upgrade added chamfers, baked vertex AO, smoothed normals, UVs and procedural detail textures. The old v1 limitations about having no UVs/textures are superseded.
- The 15.6941 m full-file length includes the optional static nose beam; the vehicle hull itself is about 8.53 m long. The beam is currently in the primary GLB and stretches well beyond the vehicle in the preview. Do not scale the whole model to compensate; remove or shorten the beam in a reviewed candidate.
- The measured hull/full-export height is 3.851 m versus the design target of 3.1 m. Width is 4.28 m versus about 4.2 m. Side pods remain partly hidden from the side.
- The v2 preview shows a much richer surface than v1, but its repeated detail pattern and bloom look busy at the preview scale. Review texture contrast and gameplay-distance readability before acceptance.
- Thrusters and hatch are not separate moving parts; no wear is included. The software preview is not an engine render.

## v1 to v2 evidence
The genuine v1 preview/export is preserved at baseline commit `319b25270be6d14ac3cb06caa1cfc9b8736fcc71`; v2 is committed at `8a2f69df3f8524482faecf69f8cd67a0cd7e7c5e`. Local parsing in the 2026-10-27 audit confirmed v1 at 2,032 triangles, 5 meshes/materials, no textures, bounds 4.28 x 3.76 x 8.53 m; v2 at 6,254 triangles, 9 meshes/materials, 2 textures, bounds 4.28 x 3.851 x 15.6941 m. Both GLB containers parsed and both had finite accessor bounds. The added chamfers, ambient occlusion and surface detail improve finish; the enlarged bounds are driven by optional FX, and the height and side-pod visibility remain review items. No Studio result is claimed.

