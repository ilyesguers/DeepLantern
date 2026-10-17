# Deep Lantern — Project State

Last reviewed: 2026-10-17

## Asset uploader hardening (CI passed)
- `Assets/Textures/TEXTURES/_generators/upload_assets.py` now performs a no-network preflight, validates selected paths and existing IDs, checks required creator configuration before upload, uses request timeouts and bounded retries for safe/idempotent requests (non-idempotent upload POSTs are not automatically retried), polls operation status with a configurable limit, and atomically saves progress and updates `AssetIds.luau` after each successful upload.
- `.github/workflows/texture-qa.yml` runs the uploader with `--dry-run` so file/path issues are caught without credentials or network calls.
- This hardening has not been verified against Roblox Open Cloud. The uploader still requires a separate live-account test; never commit API keys. Asset upload and Roblox Studio playtesting remain unverified.

## Status
This repository is the documentation, AI workflow, and source-asset home for the existing Roblox project. The current Studio place and local .rbxl files must be inspected directly before making implementation claims. GitHub does not automatically synchronize with Roblox Studio.

Archive integration status: 545 new paths from the supplied AI Programmer Pack and texture archive were committed to the integration branch. The texture manifest exists at `Assets/Textures/TEXTURES/manifest.json`. Seventeen differing existing documentation files were preserved and their useful unique guidance reconciled into the current versions. The imported assets have not yet been verified by importing/previewing them in Roblox Studio. Do not claim in-game validation until performed.

## Approved design
GDD Parts 1–10 are approved/locked. There is no Part 11. Approved GDD remains the product source of truth.

## Core loop
PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER.

## Locked product rules
- Exactly two currencies: Credits and Research Data.
- Station processes player-found discoveries; no passive tycoon currency generation.
- Active exploration and knowledge over RNG.
- No loot boxes/gacha, rebirths, station resets, permanent destruction, or full wipes.
- Fair failure via emergency ballast rescue; unsecured cargo may be lost.
- No grid inventory or weight-ratio math.
- Robux not for depth progression, Research Data, or high-tier power stats; cosmetics/social perks/mild convenience only.
- Tone: wonder, scale, atmosphere and eerie mystery; no horror jump scares or gore.
- Solo parity; co-op target 2–4 players.
- Mobile and low-end PC first-class.
- MVP zones: Station, Shallows, Kelp Forest, Twilight Reef.
- Correct identifier: `Zone_TwilightReef`, not `Zone_2_Twilight_Trench`.
- Currents use lightweight triggers/scripts, not per-frame fluid simulation.

## Known project history (verify before editing)
- Existing Roblox place contains station and submarine-related gameplay; do not rebuild from scratch.
- A prior HUD polish pass changed only `StarterPlayer.StarterPlayerScripts.Client.Controllers.DiveHUDController`; desktop/mobile layouts were visually checked at several resolutions. DIVE ACTIVE/RETURNING states, Journal/Debrief toggles, and touch controls were not fully verified in that pass.
- A docking/return edge case involving Scout lower envelope proximity to the docking pad was deferred. Do not revisit unless requested.
- Last known station color/material edits were unsaved: `Workspace.Station.ArrivalBay.ArrivalSpawn` material Plastic→SmoothPlastic and color (163,162,165)→(112,142,162); `Workspace.Station.ArrivalBay.Floor` color (95,135,105)→(58,94,112). These are historical notes; inspect the current place before relying on them.

## Backup safety
- `save.rbxl` is the original and must never be overwritten.
- `DeepLantern_Backup_Oct09.rbxl` is a backup and must never be overwritten.
- Before any edit, create/use a separately named working copy and confirm it is the one open in Studio.
- Do not save or publish without explicit user approval.

## Agent status
Start with an inspection-only Studio session. Report verified state, unknowns, and the smallest safe next task. Never claim Studio was inspected unless the MCP/Studio tool actually worked.


## Roblox Studio import readiness
- Added `Roblox/STUDIO_IMPORT_GUIDE.md` documenting the expected Explorer hierarchy for the texture UI modules and a safe demo smoke test.
- The repository still does not include a live `.rbxl`/`.rbxlx` place. Fusion version compatibility, actual asset uploads, and runtime behavior must be verified in Studio.
