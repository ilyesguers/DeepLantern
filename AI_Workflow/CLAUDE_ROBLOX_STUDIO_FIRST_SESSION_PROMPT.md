# Claude + Roblox Studio — First Session Prompt

Use this prompt when Claude is connected to Roblox Studio and can access this repository.

---

You are joining **Deep Lantern**, an existing Roblox underwater exploration game. This is not a blank project. Your job today is to understand the real project state safely, not to rebuild it.

## Required onboarding

Before proposing implementation, read these repository files in this order:

1. `README.md`
2. `AI_START_HERE.md`
3. `PROJECT_STATE.md`
4. `GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt` — all approved parts, Parts 1–10 only
5. `Docs/IMPLEMENTATION_NOTES.md`
6. `AI_Workflow/AI_AGENT_RULES.md`
7. `AI_Workflow/FILE_MAP.md`
8. `AI_Workflow/ROBLOX_STUDIO_MCP_CHECKLIST.md`
9. `AI_Workflow/ROBLOX_UI_SKILL_SETUP.md`
10. `Roblox/STUDIO_IMPORT_GUIDE.md`
11. Relevant changelog and handoff/task templates.

Then inspect the **currently open Roblox Studio place** through the connected Studio tools. Do not infer the live place from repository notes alone. Confirm the connection actually works before saying you inspected Studio.

## Non-negotiable safety rules

- **First session is inspection-only. Do not edit anything yet.**
- Do not create, delete, rename, reparent, or rewrite instances/scripts during this first session.
- Do not run mutating code, save, publish, or change live game settings.
- Never overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`. Any future work must use a separately named working copy and confirm that copy is the one open.
- Preserve all existing gameplay and features. Never rebuild from scratch or refactor unrelated systems for convenience.
- Do not assume GitHub automatically syncs with Studio. State exactly how repository source maps to the live place.
- Never invent paths, object names, asset IDs, dependencies, test results, or capabilities. Clearly label facts as **verified**, **reported in documentation**, **assumed**, or **not yet verified**.
- Never expose, log, commit, or request secrets/API keys in chat. Use approved secret storage only.
- If the Studio connection is unavailable, say so plainly and stop short of claiming a live inspection.

## Locked design requirements

The approved GDD Parts 1–10 are authoritative and locked. There is no Part 11.

- Core loop: **PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER**.
- Exactly two currencies: **Credits** and **Research Data**.
- The station processes discoveries the player finds; no passive tycoon income.
- Favor knowledge and active exploration over RNG. No loot boxes/gacha.
- No rebirths, station resets, permanent destruction, or full wipes.
- Fair failure uses emergency ballast rescue; unsecured cargo may be lost.
- No grid inventory or weight-ratio math.
- Robux must not buy depth progression, Research Data, or high-tier power stats.
- Tone is wonder, scale, atmosphere, and eerie mystery; no horror jump scares or gore.
- Solo parity; co-op target 2–4 players.
- Mobile and low-end PC are first-class targets.
- MVP zones: Station, Shallows, Kelp Forest, Twilight Reef.
- Correct zone identifier: `Zone_TwilightReef`.
- Currents use lightweight triggers/scripts, not per-frame fluid simulation.
- Compact functional Docking Ring is MVP; expanded/public/social functionality is post-MVP.

If the live place conflicts with documentation or the approved GDD, do not silently change either. Report the exact conflict and ask for direction.

## Inspect the live place

Without making changes, identify and report:

1. Studio connection status, current place name, and whether it is a working copy or unknown.
2. Relevant Explorer hierarchy and exact paths for:
   - station and arrival/spawn area
   - submarine, docking, and dive/return flow
   - server scripts, RemoteEvents/RemoteFunctions, client controllers, and shared modules
   - UI/HUD, data persistence, upgrades, discoveries/codex, and zone logic, where present
3. For each system, list the specific instances/scripts inspected and summarize only behavior supported by code or direct observation.
4. Existing warnings/errors visible in Output, if safely available without running or changing anything.
5. Differences between the live place and repository notes, including missing modules or dependencies.
6. Texture/UI import readiness. Repository notes say `AssetIds.luau` contains blank IDs; verify before relying on that statement. Do not invent IDs or perform uploads.
7. Which claims cannot be confirmed without Play Solo/client-server testing.

Do not run the game merely to produce a report unless the user separately authorizes testing. Do not save or publish.

## Required report format

Return a concise but useful report with these headings:

- **Connection and place identity**
- **Files/docs read**
- **Verified Explorer map**
- **Systems found and their current evidence**
- **Errors/warnings observed** (or “not inspected”)
- **Repository ↔ Studio discrepancies**
- **Unknowns and risks**
- **Recommended next 3 small tasks**, ordered by safety/priority
- **First recommended task**: exact paths/instances, intended behavior, likely risks, test plan, rollback plan, and why it is the smallest safe step

Finish by asking for approval before making any edits. Do not perform the recommended task in this session.

## Future work protocol

Only after explicit user approval for a specific task:

1. Restate scope and exact instances/files to change.
2. Create/use a separately named working copy and confirm it.
3. Make the smallest change that preserves existing behavior and public instance names/APIs.
4. Test only with the tools and environment actually available. Distinguish static inspection, Play Solo, Start Server/Start Player, mobile emulator, and published testing.
5. Report exact changes, real test results, limitations, and rollback.
6. Update `PROJECT_STATE.md` and `CHANGELOG.md` only with verified facts.
7. Do not save/publish over the original or publish to production without explicit approval.

**Your first action is reading and inspection only. Do not start building until the user approves a concrete task.**
