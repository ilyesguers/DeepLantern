# DL-002 — Modular Research Station Kit

**Priority:** P0  
**Status:** QUEUED  
**Deliverables:** modular Blender source, FBX/GLB pieces, texture folder, preview sheet, manifest.

## Goal
Build a consistent family of snap-together station modules that extend the existing station instead of replacing it. Model individual reusable pieces, not one huge uneditable building.

## Required modules
1. Pressure-rated wall panel, plain.
2. Window wall with thick frame and reinforced glass.
3. Corner wall module with matching seam language.
4. Floor tile with inset service channel.
5. Ceiling beam / structural rib.
6. Door frame with pressure seal.
7. Hatch with wheel/locking mechanism.
8. Short railing and corner railing.
9. Pipe bundle and cable tray.
10. Exterior floodlight bracket.
11. Small ventilation/filter unit.
12. Service access panel.

## Art direction
Industrial-but-welcoming ocean research outpost. Off-white enamel panels, desaturated deep blue structure, safety orange handles, cyan indicators, brushed metal details, subtle water stains near exterior edges. Make it feel maintained and lived in, not abandoned or horror-themed.

## Modular constraints
- Define one grid unit and use it consistently; all wall/floor modules must align without gaps when snapped together.
- Put origins on the intended snap point or module center and document the convention.
- Ensure wall thickness, door clearance and window proportions are consistent.
- Avoid visible seams where two standard modules meet. Use dedicated corner pieces instead of intersecting two full walls.
- Make variants through geometry (plain, damaged, reinforced), not random color swaps alone.
- Keep separate mesh objects only when needed for interaction or reuse.

## Performance and outputs
Target 500–3,000 triangles per standard module; complex hatch/window may exceed if justified. Use 1K shared textures or trim sheets where practical. Deliver one editable .blend with collections grouped by module and separately exportable meshes. Include a grid assembly preview proving pieces align.

## Validation
Build a 3×2 wall/floor test assembly; check seams, origin alignment, scale and collisions. Export/re-import each module. No import into the live place until explicitly approved.

## Generator prompt
“Professional modular underwater research station architecture kit for a stylized premium exploration game. Create separate snap-fit modular pieces: pressure-rated wall, reinforced window wall, corner wall, floor tile, ceiling rib, sealed hatch door, railing, cable tray, pipe bundle, floodlight bracket and ventilation/filter unit. Consistent modular grid, engineered proportions, thick readable forms, off-white enamel panels, deep blue structural frame, orange safety handles, restrained cyan indicator lights, subtle marine wear. Clean topology, UV-ready, game-optimized, no text, no logos, no floating pieces. Each part has a deliberate origin/pivot and must assemble seamlessly with matching dimensions.”
