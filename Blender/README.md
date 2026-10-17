# Deep Lantern — Blender Preparation Checklist

This folder defines the 3D-asset workflow for Deep Lantern. It does not mean any model is finished or imported.

## Goal for the first build session

Do not model a full station, submarine, or zone before checking the existing Roblox place. First inspect the live game in Studio, list the props/models already present, and identify one small, visible, low-risk gap that is approved by the GDD and fits the current environment.

Good first-asset candidates, only if confirmed as needed in the live place:
- a small station equipment prop;
- a compact wall-mounted console or sensor;
- a simple underwater environmental prop.

Avoid as the first task: the whole station, a full submarine, large modular architecture, rigged/animated assets, or anything that changes gameplay scale or collision-critical paths.

## Before modeling

- [ ] Read the approved GDD Parts 1–10 and relevant visual-reference notes.
- [ ] Inspect the existing Studio place and confirm the asset is actually missing or needs replacement.
- [ ] Write an asset brief using MODEL_BRIEF_TEMPLATE.md.
- [ ] Record where the model will be placed, approximate dimensions in Roblox studs, pivot/origin, expected player interaction, and whether collision is needed.
- [ ] Confirm the style, materials, and performance budget before detailed work.
- [ ] Confirm the asset is allowed by the approved design; visual references do not authorize new mechanics.

## Required deliverables

For each approved model, create Assets/Models/<AssetName>/ with:
- editable .blend source;
- export file (.fbx or another explicitly agreed format);
- README.md with purpose, dimensions in studs, pivot/origin, triangle estimate, materials/textures, collision plan, export settings, and source/license notes;
- preview PNG;
- import/test status, including the Studio place copy used and actual test results.

Do not create empty placeholder deliverables and mark them complete. If a binary model cannot be produced in the current environment, provide the brief and implementation instructions, and label the model as not yet created.

## Roblox import and verification

- [ ] Export using documented transforms, scale, axes, and units.
- [ ] Import into a separately named working copy of the place.
- [ ] Check dimensions and orientation against existing objects and player scale.
- [ ] Check pivot, collision shape, material appearance, texture paths, and visual readability.
- [ ] Check triangle/texture cost and mobile/low-end PC impact.
- [ ] Check Output for import errors and verify the asset in context.
- [ ] Record whether checks were static, visual in Studio, or playtested.
- [ ] Do not save over the original or publish without explicit user approval.

## Automation and tool safety

Blender, Roblox Studio, and GitHub are separate unless a real integration is configured and verified. Do not claim a Blender MCP connection, direct file synchronization, export, or Studio import unless it actually occurred. Do not install untrusted Blender add-ons or run unknown scripts just to enable automation.

## Status vocabulary

- **Planned** — approved brief exists; no model created.
- **In progress** — editable source work has started.
- **Exported** — an export file exists and was checked for presence, not necessarily in Studio.
- **Imported** — imported into the named working place.
- **Verified in Studio** — scale, pivot, materials, collisions, and context were actually checked.
- **Playtested** — behavior/performance was tested in a stated Studio test mode.

Never use “complete” without naming the level actually achieved.
