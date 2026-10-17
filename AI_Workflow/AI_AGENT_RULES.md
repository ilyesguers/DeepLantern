# Deep Lantern — AI Agent Rules

## Source of truth
Approved GDD Parts 1–10 are authoritative and locked. Project-state notes describe verified implementation reality but do not override design. Implementation notes resolve only the three documented cross-part ambiguities. Visual boards communicate art direction, not production-ready assets or mechanics. If authoritative sources conflict, report the conflict and ask rather than inventing a decision.

## Required reading order
1. `PROJECT_STATE.md`
2. `GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt`
3. `Docs/IMPLEMENTATION_NOTES.md`
4. Relevant boards under `Art/VisualReference/`
5. This file and the task-specific workflow/checklists.

## Invariants
- Underwater exploration adventure with a functional research station; core loop: PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER.
- Exactly two currencies: Credits and Research Data.
- Knowledge and active exploration over RNG/idle income; no loot boxes/gacha, rebirths, full wipes, permanent destruction, or P2W depth progression.
- No grid inventory or weight-ratio math. Failure uses emergency ballast rescue; unsecured cargo may be lost.
- Robux must not buy depth progression, Research Data, or high-tier power stats.
- Atmospheric wonder and mystery, not horror; no jump scares or gore.
- MVP zones: Station, Shallows, Kelp Forest, Twilight Reef. Use `Zone_TwilightReef`, not `Zone_2_Twilight_Trench`.
- Compact functional Docking Ring is MVP for private co-op staging, crew boarding and submarine launch; expanded/public/social ring remains post-MVP.
- Currents use lightweight scripted/trigger modifiers, not fluid simulation or per-frame environmental physics.
- Codex stages: Sighted → Scanned → Studied → Mastered.
- Solo parity; co-op target 2–4 players. Mobile and low-end PCs are first-class targets.

## Safe edits
Inspect first; propose exact paths and expected behavior; wait for approval. Keep scope small, preserve instance names/public APIs, and do not delete/rename objects for convenience. Never edit/save over `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`; use a separately named working copy. Do not save/publish without explicit approval. Validate Luau and client/server responsibilities. Never invent asset IDs, paths, access, or test results. Do not commit credentials/secrets.

## Visual direction
Use deep-ocean navy/blue, restrained cyan/bioluminescent accents, readable silhouettes, purposeful station machinery and consistent materials/scale. Do not use an entire reference board as a finished UI texture. Build responsive Roblox UI objects and test landscape/portrait.

## Handoff
Every completed task must update `PROJECT_STATE.md` and `CHANGELOG.md` with verified facts, exact paths, tests and remaining issues. Never mark work complete while required assets/source files are missing.