# Claude workflow: create real models in Roblox Studio (no Blender)

This repo is the source of truth for the existing Deep Lantern Roblox game. Use the user's linked skill repo as an aid, not as permission to rewrite the game:
- https://github.com/afrxo/roblox-agent-skills — Luau, Roblox runtime/toolchain, and UI skills.
- The screenshot shows skills/roblox-ui/SKILL.md; it is guidance for UI/Fusion, not a 3D model generator and not a Studio connection by itself.
- For actual in-Studio construction, Claude needs an enabled, verified Roblox Studio MCP/agent connection. A GitHub repo connection alone cannot insert Instances into an open Studio place.

## Start each session
1. Read AI_START_HERE.md, PROJECT_STATE.md, approved GDD Parts 1–10, Docs/IMPLEMENTATION_NOTES.md, AI_Workflow/AI_AGENT_RULES.md, and Blender/MODEL_FACTORY/README.md (the queue name is historical; do not use Blender).
2. Check whether a real Studio MCP tool is available and call its studio-list function. Record evidence. If no Studio connection is available, stop short of claiming model creation; build/review source-side Luau builder scripts and give the user the smallest setup step needed.
3. Inspect the current place and exact Explorer paths before edits. Never overwrite save.rbxl or DeepLantern_Backup_Oct09.rbxl. Work only in a separately named copy, e.g. DeepLantern_ModelFactory_WorkingCopy. Never publish the live game without explicit approval.
4. Preserve all existing gameplay, scripts, attachments, attributes, currencies, UI, GDD decisions, and names. Do not rebuild the game. Current product invariants: Credits and Research Data only; PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER; zones Station, Shallows, Kelp Forest, Twilight Reef; exact ID Zone_TwilightReef; wonder/mystery, not horror; mobile/low-end PC first.

## Build route without Blender
Create models directly as organized Roblox Studio Instances using carefully designed Parts, wedges, cylinders, spheres, beams, attachments, SurfaceAppearance or verified mesh/texture assets when available. Build visually layered, intentional props, not piles of default blocks. MeshParts must only be used if there is a real authorized mesh asset. Do not fabricate texture IDs or claim Parts are mesh geometry.

For every asset:
- Inspect existing equivalent assets and reuse/upgrade rather than duplicate.
- Give a coherent silhouette and believable construction: shell, trim, panel breaks, recessed areas, fasteners, handles, ports, lenses, brackets and base/support as appropriate. Avoid excessive tiny pieces and floating decorations.
- Keep palette consistent: deep ocean blue/teal/indigo, controlled cyan emissives, restrained coral-orange accents; readable at game camera distance and in dim water.
- Keep static props anchored; set collision/query/touch deliberately; provide stable pivot/origin and sensible bounding box. No art-only scripts. Avoid unneeded physics, per-frame effects, excessive lights/particles, and huge Part counts.
- Use exact names, parent into a dedicated folder, and add attributes only when they serve existing systems. Never add new gameplay mechanics or change currencies/progression as part of asset work.
- Inspect/read back the created model after every construction step. Test scale, camera readability, collisions, clipping, lighting, mobile performance and intended placement. Use Studio playtest/log/screenshot tools only if actually available.
- Export .rbxm/.rbxmx if supported and put the export/source builder/manifest into GitHub. Keep screenshots as evidence only if actually captured. Report exact Part count and actual tests, not estimates presented as verified facts.

## Queue order
Use the existing 20 briefs in Blender/MODEL_FACTORY/TASKS/ as design requirements but translate each to a Studio-native model workflow:
P0: DL-001 research submarine; DL-002 research station kit; DL-003 dive beacon; DL-004 sample canisters; DL-005 research console.
P1: DL-006 coral family; DL-007 kelp cluster; DL-008 seafloor rocks; DL-009 bioluminescent flora; DL-010 wreckage set; DL-011 Twilight Reef arch; DL-012 ancient relic; DL-013 discovery display; DL-014 docking pad; DL-015 cave entrance.
P2: DL-016 cable kit; DL-017 signage kit; DL-018 research crates; DL-019 small fauna; DL-020 lighting kit.
Create asset variants only when they share a coherent reusable kit and remain performant.

## Status tracking
For each asset record: ID, status (QUEUED / BLOCKED / IN_PROGRESS / BUILT_UNVERIFIED / VERIFIED), Studio location, export/source path, actual Part count, verified dependencies, pivot/scale, collision notes, performance notes, checks performed, evidence paths, known issues, rollback. VERIFIED requires read-back from Studio and the stated checks. Never mark a model complete merely because a prompt/spec or Luau script exists.

## GitHub safety
Work on a feature branch and small commits. Never modify main directly. Do not commit secrets, access tokens, private place files, or user credentials. Review third-party Creator Store assets for suspicious scripts (require with numeric IDs, loadstring, getfenv, HTTP loaders) before keeping them. If an external skill's guidance conflicts with this repo's GDD or integration policy, this repo wins.

## If Studio MCP is unavailable
Create Luau builder modules/scripts under Roblox/ModelFactory/Source/ that are idempotent, build only under Workspace.DeepLantern_ModelFactoryPreview, never clear unrelated Workspace children, never overwrite existing models, and include a preview/cleanup function limited to that dedicated folder. Provide a manifest and instructions for running in a named working copy. Do not claim these scripts were executed. Ask the user only for the missing Studio connection step, not for repeated project details.