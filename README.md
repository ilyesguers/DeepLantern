# Deep Lantern

**Underwater exploration-adventure for Roblox**  
Repository for the approved game design, AI-assisted development workflow, visual direction, and future production assets.

> **Safety first:** This repository does not automatically synchronize with Roblox Studio. Never overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`. Work on a separately named copy and do not save or publish without explicit user approval.

## Start here
1. [AI Start Here](AI_START_HERE.md) — mandatory onboarding.
2. [Project State](PROJECT_STATE.md) — known design and implementation context.
3. [Approved GDD index](GDD/DeepLantern_GDD_APPROVED_SUMMARY.md) — quick summary; the full approved GDD Parts 1–10 remains authoritative.
4. [Implementation Notes](Docs/IMPLEMENTATION_NOTES.md) — implementation clarifications.
5. [AI Agent Rules](AI_Workflow/AI_AGENT_RULES.md) — non-negotiable invariants.
6. [Codex first-session prompt](AI_Workflow/CODEX_FIRST_SESSION_PROMPT.md) — inspection-only; no changes.
7. [File Map](AI_Workflow/FILE_MAP.md) — folder purposes.

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
- Correct zone identifier: `Zone_TwilightReef`.
- Currents use lightweight triggers/scripts, not per-frame fluid simulation.

## Workflow
**Inspect → propose → user approves → implement small change → test → report → update handoff.**

No AI agent may claim it inspected Studio, imported assets, or passed tests unless it actually did so. Visual references communicate art direction; they are not production-ready textures or models and do not override the GDD.

## Integrations
- [Official Roblox Studio Agent Plugin](https://github.com/Roblox/roblox-studio-agent-plugin)
- [Roblox Agent Skills (including roblox-ui)](https://github.com/afrxo/roblox-agent-skills)

See [Studio MCP checklist](AI_Workflow/ROBLOX_STUDIO_MCP_CHECKLIST.md), [UI skill setup](AI_Workflow/ROBLOX_UI_SKILL_SETUP.md), and [Blender asset pipeline](Blender/ASSET_PIPELINE.md).

## Asset status
Reference boards, the complete approved GDD source files, and production model/texture assets should be committed only after they are verified and organized. A summary is not a replacement for the full GDD. Do not invent missing files or mark an asset as production-ready without validation.

## Changes
See [CHANGELOG](CHANGELOG.md). Use [Codex task template](AI_Workflow/CODEX_TASK_TEMPLATE.md) and [agent handoff template](AI_Workflow/AGENT_HANDOFF_TEMPLATE.md) for every scoped task.
