# Changelog

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
