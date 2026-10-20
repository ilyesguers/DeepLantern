# DL-006 — Stylized Coral Family
**Priority:** P1 · **Status:** QUEUED

## Goal
Create five distinctive coral silhouettes that can be combined into rich reef compositions without looking like repeated copies: branching fan, rounded brain coral, plate coral, tubular coral, and compact mound coral.

## Art direction
Colorful and luminous but biologically inspired: coral pink, warm orange, violet, pale mint, turquoise and restrained deep-blue shadow. Use a cohesive roughness/material language and vary color by species, not by random noise. Silhouettes must remain readable against dark water. Include subtle pores, ridges, polyps or layered plates where they contribute to shape.

## Geometry/performance
Aim 1k–5k triangles per asset; use geometry for silhouette and bake fine pores/ridges. Avoid millions of faces, dense voxel remeshes, hair-thin branches and excessive subdivision. Make each coral a separate object with base pivot at seafloor contact. Provide 2–3 scale variants only when the silhouette remains credible.

## Outputs and validation
One organized .blend, separately exportable assets, shared texture atlas/materials where practical, preview sheet with all five assets, manifest and triangle counts. Check flat base contact, non-manifold edges, normals, material paths, and export/re-import.

## Generator prompt
“Create a premium stylized underwater coral family for a colorful exploration game: five separate silhouettes including branching sea fan, rounded brain coral, layered plate coral, thick tubular coral and compact mound coral. Rich controlled coral pink, orange, violet, mint and turquoise accents; detailed organic ridges and polyps; beautiful readable forms against deep ocean water; artistically coherent species design; clean game-ready topology with fine detail baked where appropriate; UV-ready PBR; no rock base attached; no millions of polygons; no thin fragile tips. Each piece has a stable bottom pivot and can be combined into a modular reef.”