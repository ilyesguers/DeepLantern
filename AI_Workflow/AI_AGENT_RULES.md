# Deep Lantern — AI Agent Rules

## Source of truth
Approved GDD Parts 1–10 and project-state notes are authoritative. If sources conflict, report the conflict and stop; do not silently invent a decision. Art boards communicate visual direction, not final mechanics or production-ready assets.

## Invariants
- Underwater exploration adventure with a functional research station.
- Core loop: PLAN → DIVE → DECIDE → DEBRIEF → UPGRADE → GO DEEPER.
- Exactly two currencies: Credits and Research Data.
- Knowledge over RNG; no gacha, loot boxes, or tiny-probability progression.
- No passive tycoon income, rebirths, station resets, full wipes, or permanent destruction.
- Failure uses emergency ballast rescue; unsecured cargo may be lost.
- No grid inventory or weight-ratio math.
- Robux only for cosmetics, social perks, and mild convenience—not depth progression, Research Data, or high-tier power stats.
- Atmospheric wonder and mystery; no horror jump scares or gore.
- Solo parity, co-op target 2–4; support mobile and low-end PCs.
- MVP zones: Station, Shallows, Kelp Forest, Twilight Reef.
- Correct zone identifier: `Zone_TwilightReef`.
- Currents use lightweight triggers/scripts, not per-frame fluid simulation.
- No free swimming at launch unless approved GDD explicitly says otherwise.

## Safe edits
Inspect first; propose exact paths and expected behavior; make smallest approved change; preserve instance names and public APIs; do not delete/rename objects for convenience; do not save/publish without explicit approval; never invent asset IDs, paths, access, or test results. Validate Luau and client/server responsibilities. Report changes, tests actually run, risks, rollback, and unsaved changes.