# File Map and Asset Contract

| Path | Purpose | Authority / status |
|---|---|---|
| `GDD/DeepLantern_GDD_Parts_1-10_APPROVED.rtf` | Original approved GDD | Design source of truth |
| `GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt` | Readable text export for AI | AI-readable copy; compare with RTF if conversion concerns arise |
| `GDD/DeepLantern_GDD_APPROVED_SUMMARY.md` | Quick summary | Navigation aid only; never overrides full GDD |
| `PROJECT_STATE.md` | Implementation handoff | Must reflect verified reality; never overrides GDD |
| `ASSET_READINESS.md` | Asset inventory, statuses and verification gates | Current asset-readiness checklist |
| `Docs/IMPLEMENTATION_NOTES.md` | Cross-part clarifications | Clarifications only |
| `Art/VisualReference/*.png` | Ten canonical visual reference boards | Style inspiration, not production assets |
| `VISUAL_REFERENCE/` | Legacy duplicate reference boards | Retained temporarily for old links; do not add new boards here |
| `Assets/Textures/TEXTURES/manifest.json` | Texture/UI/VFX manifest | File and metadata index; keep aligned with the pack |
| `Assets/Textures/TEXTURES/` | Generated texture maps, icons, UI/VFX, previews, Luau and generators | Repository-ready; Studio import and runtime remain separate validation steps |
| `Assets/Textures/TEXTURES/luau/AssetIds.luau` | Roblox-hosted image IDs | Blank IDs are unresolved; never invent IDs |
| `Assets/Models/` | Future production model exports | Intentionally deferred; do not assume models exist |
| `Blender/` | Future Blender pipeline guidance | Documentation only until model work begins |
| `Roblox/` | Studio integration and import guidance | Follow using a separately named working copy |
| `AI_Workflow/` | Agent rules, prompts, setup and checklists | Read before agent work |
| `CHANGELOG.md` | Human-readable change history | Record meaningful verified repository changes |

## Asset naming and readiness rules

- Use descriptive ASCII filenames and one extension; do not create ambiguous `final-final` variants.
- New future models should use `Assets/Models/<ModelName>/` with source, export, preview, README, scale/pivot/collision notes and Studio import status.
- For new textures, record dimensions, intended use, color-space expectations and source/license only when known.
- Keep visual reference boards separate from production texture maps and UI assets.
- Before an asset is marked game-ready, verify its path, manifest entry, runtime ID if hosted, and Studio behavior. Repository presence alone is not game readiness.
- Do not delete byte-identical files automatically. Duplicate images can be legacy links; repeated texture maps or icons can be intentional.
- Never overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`.
