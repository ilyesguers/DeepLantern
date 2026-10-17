# Deep Lantern

**Underwater exploration-adventure for Roblox**  
Repository for the approved game design, AI-assisted development workflow, visual direction, and source assets.

> **Safety first:** This repository does not automatically synchronize with Roblox Studio. Never overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`. Work on a separately named copy and do not save or publish without explicit user approval.

## Start here
1. [AI Start Here](AI_START_HERE.md) — mandatory onboarding.
2. [Project State](PROJECT_STATE.md) — known design and implementation context.
3. [Approved GDD source (text)](GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt) — readable approved Parts 1–10.
4. [Implementation Notes](Docs/IMPLEMENTATION_NOTES.md) — implementation clarifications.
5. [AI Agent Rules](AI_Workflow/AI_AGENT_RULES.md) — non-negotiable invariants.
6. [Codex first-session prompt](AI_Workflow/CODEX_FIRST_SESSION_PROMPT.md) — inspection-only; no changes.
7. [File Map](AI_Workflow/FILE_MAP.md) — folder purposes.
8. [Roblox Studio import guide](Roblox/STUDIO_IMPORT_GUIDE.md) — exact Explorer hierarchy and a safe UI smoke test.

## Project identity
Deep Lantern is an exploration-first underwater adventure with a functional research station. The station processes discoveries found by players; it is not a passive tycoon.

**Core loop:** PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER.

## Locked design constraints
- Exactly two currencies: Credits and Research Data.
- Knowledge over RNG; no loot boxes/gacha or tiny-probability progression.
- No passive tycoon income, rebirths, station resets, permanent destruction, or full wipes.
- Fair failure via emergency ballast rescue; unsecured cargo may be lost.
- No grid inventory or weight-ratio math.
- Robux must not buy depth progression, Research Data, or high-tier power stats.
- Wonder and eerie mystery, not horror; no jump scares or gore.
- Solo parity; co-op target 2–4 players.
- Mobile and low-end PCs are first-class targets.
- Compact functional Docking Ring is MVP; expanded/public/social functionality is post-MVP.
- Correct zone identifier: `Zone_TwilightReef`.
- Currents use lightweight triggers/scripts, not per-frame fluid simulation.

## Workflow
**Inspect → propose → user approves → implement small change → test → report → update handoff.**

No AI agent may claim it inspected Studio, imported assets, or passed tests unless it actually did so. Visual references communicate art direction; they are not production-ready textures or models and do not override the GDD.

## Assets and validation
- Approved GDD sources are under `GDD/`; visual boards are under `Art/VisualReference/`.
- Imported texture pack: [texture README](Assets/Textures/TEXTURES/README.md), [Arabic README](Assets/Textures/TEXTURES/README.ar.md), [manifest](Assets/Textures/TEXTURES/manifest.json).
- The archive import was verified in GitHub Actions, including ZIP integrity and manifest presence. This does not mean every texture has been imported or tested in Roblox Studio.
- Production models must include editable source/export, preview, scale/pivot/collision notes and Studio import status.

## Integrations
- [Official Roblox Studio Agent Plugin](https://github.com/Roblox/roblox-studio-agent-plugin)
- [Roblox Agent Skills (including roblox-ui)](https://github.com/afrxo/roblox-agent-skills)

See [Studio MCP checklist](AI_Workflow/ROBLOX_STUDIO_MCP_CHECKLIST.md), [UI skill setup](AI_Workflow/ROBLOX_UI_SKILL_SETUP.md), and [Blender asset pipeline](Blender/ASSET_PIPELINE.md).

## Changes
See [CHANGELOG](CHANGELOG.md). Use [Codex task template](AI_Workflow/CODEX_TASK_TEMPLATE.md) and [agent handoff template](AI_Workflow/AGENT_HANDOFF_TEMPLATE.md) for every scoped task.
