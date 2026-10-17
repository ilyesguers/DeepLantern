# Deep Lantern — AI Start Here

This is an existing Roblox project, not a blank template. Approved GDD Parts 1–10 and the current project state are the source of truth.

## Read first
1. `PROJECT_STATE.md`
2. Approved GDD Parts 1–10
3. `Docs/IMPLEMENTATION_NOTES.md`
4. `AI_Workflow/AI_AGENT_RULES.md`
5. `AI_Workflow/CODEX_FIRST_SESSION_PROMPT.md`

## First session: inspection only
Verify the Roblox Studio Agent/MCP connection. Inspect the open place, exact Explorer paths, scripts and current behavior. Report confirmed facts separately from assumptions. Do not edit, create, delete, rename, save, publish, or run mutating code. Wait for approval.

## Non-negotiable safety
Never overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`. Use an explicitly named working copy. Never claim Studio access or tests unless actually verified.

## Game invariants
- Exactly two currencies: Credits and Research Data.
- Core loop: PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER.
- Knowledge over RNG; no loot boxes/gacha or tiny-probability progression.
- No passive tycoon income; station upgrades are functional.
- No rebirths, station resets, permanent destruction, or full wipes.
- Robux cannot buy depth progression, Research Data, or high-tier power stats.
- Tone is wonder and eerie mystery, not horror; no jump scares or gore.
- Solo parity; co-op target 2–4 players.
- Mobile and low-end PC are first-class targets.
- Correct zone identifier: `Zone_TwilightReef`.
- Currents use lightweight triggers/scripts, not per-frame fluid simulation.
- Visual references guide style, not unapproved gameplay mechanics.

Before changes: state exact paths, risk, and tests. After approved changes: report exact diffs, actual test results, limitations, rollback, and unsaved Studio state.