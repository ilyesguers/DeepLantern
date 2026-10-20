# Deep Lantern — 3D Model Factory

This folder defines a safe, repeatable queue for producing real 3D assets for the existing Roblox game. It does not replace the game, alter its gameplay, or claim that a model exists until its native source/export files have been created and validated.

## Required reading
1. `../../AI_START_HERE.md`
2. `../../PROJECT_STATE.md`
3. `../ASSET_PIPELINE.md`
4. `MODEL_QUEUE.md`
5. The individual brief under `TASKS/` before modeling that asset.

## Target art direction
Stylized premium underwater exploration: readable silhouettes, rich layered materials, strong focal details, believable construction, saturated but controlled cyan/teal/indigo with coral orange and bioluminescent accents. Wonder and eerie mystery, never horror. Models should look authored, not like piles of generic primitives.

## Production rules
- Build one asset/task at a time; finish, validate and record it before moving to the next.
- Preserve all existing files. Do not overwrite source assets or edit the original Roblox place.
- Keep source `.blend`, exported `.fbx` or `.glb`, texture maps, preview renders and a manifest together for each finished asset.
- Prefer reusable modular pieces and shared materials where that does not make assets visually repetitive.
- Keep real-time budgets in mind: LOD-friendly silhouette, controlled triangle count, few materials, sensible texture resolution, no hidden geometry, no unnecessary modifiers, no extreme subdivision.
- Roblox import scale: use meters consistently in Blender and document the chosen Roblox studs conversion; test scale and pivot in a separate test place before use.
- Apply transforms before export; set origin/pivot intentionally; name objects/materials clearly; use packed textures or a documented relative texture folder.
- Do not bake text into textures if it needs to be localized or changed in-game. Use geometry/decal/UI where appropriate.
- Never claim Roblox Studio validation unless it was actually run. Never upload or publish assets to Roblox without explicit approval and valid account credentials.
- Use only assets the project owns or that have explicit commercial/game-use rights. Never bypass paid export gates or subscriptions.
- If an external text-to-3D generator is unavailable, use Blender procedural modeling only when it can meet the visual brief. Mark the limitation instead of calling a crude placeholder “professional.”

## Completion checklist
For every asset:
1. Inspect the relevant game context and existing asset folders.
2. Produce a written blockout plan and key dimensions.
3. Create the native Blender source.
4. Model primary silhouette, secondary forms, tertiary surface detail, materials and lighting for preview.
5. Optimize topology and remove hidden/unneeded parts.
6. Validate mesh integrity, scale, pivot, material/texture paths and export re-import.
7. Export FBX and/or GLB with clear filenames.
8. Render front, side, back and three-quarter previews.
9. Record triangle count, texture sizes, format, scale, pivot, limitations and validation evidence in the manifest.
10. Commit the asset and its status note on the working branch. Continue to the next queue item.

## Status meanings
- `QUEUED`: brief written; no model produced yet.
- `BLOCKED`: needs a missing tool, generator, local Blender runtime, or license check.
- `IN_PROGRESS`: model work has actually begun.
- `BUILT_UNVALIDATED`: files created, but validation incomplete.
- `VALIDATED_EXPORT`: source and exported asset re-import checks passed.
- `STUDIO_TESTED`: imported and inspected in Roblox Studio, with evidence.
