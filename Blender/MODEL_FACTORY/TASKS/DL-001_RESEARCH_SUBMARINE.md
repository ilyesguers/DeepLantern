# DL-001 — Deep-Diving Research Submarine

**Priority:** P0  
**Status:** QUEUED  
**Deliverables:** `.blend`, `.fbx` or `.glb`, texture folder, 3–5 preview renders, manifest.

## Goal
Create the signature player submarine for Deep Lantern: a compact, robust, believable research craft with a memorable silhouette that remains readable at gameplay camera distance. It must feel engineered for repeated dives, repairable, and purpose-built—not a generic yellow toy submarine and not a military weapon.

## Visual design
- Primary silhouette: compact elongated pressure hull with a slightly flattened lower keel, rounded but deliberate transitions, reinforced front viewport assembly, rear propulsion pod(s), and stable side-mounted buoyancy housings.
- Front: large protected observation dome or thick multi-pane viewport, metal retaining ring, small optical/sensor cluster and two compact work lights.
- Top: low-profile equipment rail, antenna/sonar mast, one clearly readable access hatch and lifting points.
- Sides: restrained hazard markings, replaceable armor panels, inspection seams, grab rails and service connectors.
- Rear: guarded thrusters with visible nozzle depth, cable routing and a believable service panel. No exposed spinning blade geometry that becomes unreadable at small scale.
- Color palette: deep navy/graphite hull, warm off-white panels, high-visibility orange safety parts, cyan/teal emissive instrument accents. Keep emissive surfaces small and intentional.
- Surface wear: subtle edge wear, controlled scratches, faint salt/mineral deposits and slight panel color variation. No excessive grunge.

## Shape language and craftsmanship
Use large forms first, then medium panels, then selected fine details. Every small detail must support scale or function. Avoid uniform bevels on every edge, excessive bolts, thin floating greebles, coplanar surfaces, and purely decorative pipes with no endpoints.

## Roblox/performance target
- Target roughly 8k–20k triangles for the hero mesh after optimization; if separate moving components are needed, report each component separately. This is a target, not permission to destroy silhouette quality.
- Keep materials to 4–6 where possible. Use a 2K texture set only if it materially improves the close-up; otherwise 1K. Prefer packed ORM maps only if the export/import pipeline supports them.
- Separate body, viewport, thruster assemblies, lights and movable hatch only if useful for Roblox interaction or animation.
- Use a clear centerline and pivot at the craft's intended vehicle root; document forward/up axes and bounding dimensions.
- Keep glass visually clear and robust at distance; no opaque black viewport.
- Do not include physics scripts or gameplay code in the mesh task.

## Required outputs
1. Editable Blender source with organized collections and named materials.
2. Roblox-ready FBX or GLB export with applied transforms and documented axis/scale.
3. Base color, normal and roughness/metallic maps if used, with packed/relative paths.
4. Front, side, rear and three-quarter renders on neutral background, plus one underwater hero render.
5. Manifest with triangle count, dimensions, pivot, texture sizes, export settings and validation status.

## Validation
Inspect silhouette at 10%, 25%, and 100% preview scale; check normals, non-manifold geometry, overlapping shells, shading artifacts, material paths, export/re-import and pivot. Ensure the front reads clearly and propulsion remains distinguishable. Test only in a separate Roblox Studio test place; do not modify the original game place.

## Prompt for a text-to-3D generator
“Create a polished, game-ready stylized deep-sea research submarine for a premium Roblox underwater exploration adventure. Compact elongated pressure hull, protected large forward observation dome with thick metal rim, paired guarded rear thrusters, small cyan sensor lights, practical side buoyancy housings, top sonar mast and access hatch, service panels, restrained orange safety markings, navy graphite and warm off-white materials. Authored professional silhouette, layered primary/secondary/tertiary forms, clean readable topology, realistic engineering logic, no weapons, no text logos, no floating details, no thin fragile parts. Designed for real-time third-person gameplay, optimized low-to-mid poly, baked detail where possible, clean UVs, PBR materials. Produce a coherent single asset with consistent scale and a centered vehicle-root pivot.”
