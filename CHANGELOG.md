# Changelog

## 2026-10-18 — Asset readiness documentation
- Added a verified asset-readiness checklist and clarified the canonical visual-reference folder.
- Corrected outdated visual-reference README wording that implied the boards were not yet committed.
- Preserved duplicate/legacy files; no images or other assets were deleted or renamed.
- No Roblox Studio place was modified; visual inspection of all images, Roblox uploads and in-Studio runtime tests remain pending.


## 2026-10-17 — Fusion UI dependency clarification
- Confirmed the UI modules use the Fusion 0.3 scoped-constructor API and documented the explicit `elttob/fusion@0.3.0` dependency recommendation with official source and documentation links.
- Updated the Studio import guide and project state to distinguish source-level API compatibility from actual Studio runtime verification.
- No game scripts or live Roblox place were changed; Studio testing and asset uploads remain unverified.

## 2026-10-17 — Roblox asset uploader hardening (CI passed)
- Added preflight checks for texture paths, duplicate entries and asset ID formats; dry-run mode performs no network calls or writes.
- Added explicit credential/creator validation, bounded request timeouts, retries for safe/idempotent requests, operation polling limits, error reporting, and atomic progress/source-file writes.
- Added a credential-free uploader dry-run to the texture QA workflow.
- CI passed for texture validation, manifest references and uploader dry-run. Live Roblox Open Cloud uploads and Studio validation have not been performed.

## 2026-10-17 — Archive integration
- Imported 545 new files from the supplied AI Programmer Pack and texture archive into the integration branch.
- Added the approved GDD source files, visual reference boards, and texture pack under `Assets/Textures/TEXTURES/`.
- Preserved 17 pre-existing documentation files where the archive versions differed; merged useful project-specific clarifications into the existing docs instead of blindly overwriting them.
- GitHub Actions verified ZIP integrity and the presence of the texture manifest. Roblox Studio import/playtesting remains unverified; imported textures are not yet certified as tested in-game.

## Repository AI onboarding
- Added agent onboarding, inspection-only Codex first-session prompt, safe editing rules, GitHub workflow, Studio MCP checklist, UI skill setup, file map, change checklist, Blender asset pipeline, and handoff template.
- No Roblox place file was changed, saved, or published by this documentation update.

## 2026-10-17 — Studio import readiness
- Added `Roblox/STUDIO_IMPORT_GUIDE.md` with the expected Explorer hierarchy, Fusion dependency caveat, safe asset-ID guidance and a UI smoke-test checklist.
- No Studio runtime or live upload test is claimed.
