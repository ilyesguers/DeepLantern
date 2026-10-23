# Deep Lantern — GitHub-first 3D Model Factory (No Blender)

This is the workflow for creating 20 planned asset groups. Do not connect to Roblox Studio; GitHub is the delivery location. Roblox Studio import/inspection is a later stage.

## Mandatory first steps
1. Read this file, PROMPT.md, PROGRESS.md, and GDD_COMPLIANCE_AUDIT.md before starting.
2. Read the authoritative GDD at GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt and relevant task brief under Blender/MODEL_FACTORY/TASKS/ (folder name historical; no Blender).
3. Inspect latest commits, current files, and progress; avoid duplicates. Work only on the feature branch or a new branch from it. Never commit directly to main or change unrelated game code.
4. Create one model/set at a time using a genuine authorized 3D generation tool and obtain the actual downloadable 3D file. An image, prompt, description or screenshot is not a model.
5. Commit actual source file if available, Roblox-compatible export (.fbx/.glb/.obj where supported), real required textures/maps, preview, manifest, and README under Assets/ModelFactory/Models/<ID>/.
6. Check that files exist and are non-empty. Record formats, rights/licensing and measured metadata accurately. Never invent topology counts, texture IDs, export results, or Studio tests.
7. Update PROGRESS.md after every meaningful action and after each model. Continue only after the current task is honestly marked uploaded or blocked.

## GDD authority and scope
GDD Parts 1–10 are approved/locked and always override visual briefs. Follow GDD_COMPLIANCE_AUDIT.md for the per-asset decisions.
- MVP zones only: Station, Shallows, Kelp Forest, Twilight Reef. Abyss, Lost Ruins, The Hollow, Beyond are post-MVP.
- MVP station tiers: Outpost → Station → Complex. Citadel and Deep Empire are post-MVP.
- Keep the core loop PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER and exactly two currencies: Credits and Research Data.
- Preserve existing submarine gameplay and names. Do not add new classes, controls, stats, mechanics, currencies, NPC fleets, player-built networks, GPS quest markers, passive income, gacha, creature capture inventory, combat, or extra zones.
- Compact functional Docking Ring is MVP; expanded/public/social functionality is post-MVP.
- Visual direction: deep-ocean navy/blue, restrained teal/cyan, warm amber/orange details, selective bioluminescence; wonder/mystery, not horror. Prioritize silhouette, lighting and fog over dense meshes or particle spam.
- Mobile and low-end PC are first-class. Modular reusable assets, low object counts, no unnecessary physics or per-frame effects.

## Revised queue
**P0 — core MVP anchors:** DL-001 existing Scout/submarine visual asset; DL-002 MVP station modular kit; DL-014 Sub Dock/compact Docking Ring-compatible pad; DL-005 Research Lab console; DL-003 static beacon; DL-004 sample canisters.
**P1 — MVP environment/discovery:** DL-006 coral; DL-007 kelp; DL-008 rocks; DL-009 bioluminescent flora; DL-011 Twilight Reef landmark; DL-010 small wreckage; DL-015 cave entrance pieces; DL-012 individual relic props.
**P2 — support props:** DL-013 Gallery display; DL-016 cables/hoses; DL-017 diegetic signage; DL-018 crates; DL-020 lighting fixture meshes.
**P3 — fauna:** DL-019 small non-lethal Codex fauna after confirming initial MVP needs; rigging/animation is separate and must not be claimed unless produced.

## Per-model package
- model.<actual-extension>: genuine 3D export.
- source.<actual-extension>: editable source if the tool supplies one; otherwise state why unavailable.
- Textures/: only actual required maps.
- preview.png: genuine preview, never a substitute for the model.
- manifest.json: ID, name, status, generator/source, file list, dimensions/scale/units, pivot, measured mesh stats if available, material/texture list, license/rights, import notes and limitations.
- README.md: GDD scope, brief, variants, usage, recommended import/collision settings, performance budget and limitations.

## If no 3D generator is available
Do not fake a model. Add Models/<ID>/BLOCKED.md describing the exact missing capability, preserve the prompt, mark the task BLOCKED, and update progress. GitHub stores files; it does not generate 3D geometry by itself.

## Status definitions
QUEUED, IN_PROGRESS, UPLOADED_TO_GITHUB, BLOCKED, NEEDS_REVIEW. UPLOADED_TO_GITHUB means actual model bytes are committed; it does not mean Roblox Studio validated the asset.