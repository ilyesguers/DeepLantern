# Deep Lantern — Asset Readiness Audit

Last audited: 2026-10-18
Branch: `chore/asset-readiness-audit`

This file distinguishes repository presence from verified Roblox Studio readiness. It is the current asset-preparation checklist; the approved GDD Parts 1–10 remains the design authority.

## Readiness states

- **Ready in repository:** file is present and has a documented path.
- **Needs validation:** requires visual, structural, compatibility, licensing, or Studio verification.
- **Not started / intentionally deferred:** not required for this preparation phase.

## Current inventory

| Asset group | Location | Current state | Next action |
|---|---|---|---|
| Approved GDD | `GDD/DeepLantern_GDD_Parts_1-10_APPROVED.rtf` and `.txt` | Present; authoritative design | Keep RTF as original and TXT as AI-readable copy; compare if conversion concerns arise |
| Project state and AI rules | `PROJECT_STATE.md`, `AI_START_HERE.md`, `AI_Workflow/` | Present | Update status only from verified facts |
| Visual reference boards | `Art/VisualReference/` | 10 boards present | Use this as the canonical path; see duplicate note below |
| Procedural texture/UI pack | `Assets/Textures/TEXTURES/` | 496 PNGs documented in pack README; current repository tree contains 529 paths under this pack including docs, code, generators, and data | Run QA after asset changes; verify images and UI in Studio before integration |
| Texture manifest | `Assets/Textures/TEXTURES/manifest.json` | Present | Keep manifest and file paths in sync |
| Luau UI components | `Assets/Textures/TEXTURES/luau/` | Present; syntax/CI checks are not Studio runtime proof | Check Fusion 0.3 availability and run a controlled UI smoke test in a working copy |
| Asset IDs | `Assets/Textures/TEXTURES/luau/AssetIds.luau` | Placeholders are blank until upload | Do not fill with guessed IDs; use verified uploaded asset IDs only |
| Roblox Studio guidance | `Roblox/` | Documentation present | Follow import guide only in a separate working place; no automatic sync is implied |
| Models / Blender source | `Assets/Models/`, `Blender/` | Intentionally deferred | Do not generate or expect production models during this phase |
| Audio / fonts | Not identified in current asset inventory | Not ready | Defer until the project needs and sources are defined; do not invent licenses |

## Visual reference canonical path

Use `Art/VisualReference/` as the canonical path for the 10 reference boards. The legacy `VISUAL_REFERENCE/` directory contains byte-identical copies of those 10 boards under inconsistent filenames. They are retained for now to avoid breaking links or losing provenance; do not add new reference boards to both locations. Cleanup can be considered later after repository links and history are checked.

## Duplicate-file findings

The repository tree contains groups of byte-identical blobs. Some are the two copies of visual boards; others are repeated texture-map pixels (for example flat metalness maps) or icon designs reused in different semantic slots. Identical bytes do not by themselves prove that a file is redundant: a texture or icon may intentionally be referenced at multiple paths. Therefore, no automated deletion should be based only on duplicate hashes.

## Required readiness checks before declaring assets usable in-game

1. Confirm the intended asset is listed at the expected path.
2. Confirm the manifest points to the correct file and that the file is decodable.
3. Confirm any atlas rectangle/manifest entry agrees with the actual atlas.
4. Confirm Luau keys match repository-relative asset keys.
5. For Roblox-hosted images, verify a real uploaded asset ID; blank IDs are intentionally unresolved.
6. Import/test only in a separately named Roblox Studio working copy. Verify visual quality, alpha, color space, texture tiling, UI layout, mobile scaling, and runtime output.
7. Record the result and environment in `PROJECT_STATE.md` only after the test actually succeeds.

## Safety rules

- Never overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`.
- Do not delete or rename legacy files until references and provenance have been checked.
- Do not upload assets or use credentials automatically as part of local QA.
- Never claim a Studio test, Roblox upload, or visual review that was not performed.
- GDD Parts 1–10 override visual-reference imagery wherever they conflict.
