# File Map and Asset Contract

| Path | Purpose | Authority |
|---|---|---|
| `GDD/DeepLantern_GDD_Parts_1-10_APPROVED.rtf` | Original approved GDD | Design source of truth |
| `GDD/DeepLantern_GDD_Parts_1-10_APPROVED.txt` | Readable text export for AI | Same content; verify against RTF if conversion issues appear |
| `PROJECT_STATE.md` | Implementation handoff | Must match verified reality; never overrides GDD |
| `Docs/IMPLEMENTATION_NOTES.md` | Three cross-part clarifications | Clarifications only |
| `Art/VisualReference/*.png` | Visual reference boards | Style inspiration, not production assets |
| `Assets/Textures/TEXTURES/` | Imported texture pack, maps, icons, UI and VFX assets | Follow its manifest/READMEs; Studio import still requires verification |
| `Assets/Textures/` | Texture usage guidance | Keep references separate from production texture maps |
| `Assets/Models/` | Production model exports | Include source, scale/pivot/collision notes and Studio import status |
| `Blender/` | Blender source/export pipeline guidance | No finished models implied |
| `Roblox/` | Studio integration notes | Do not assume live scripts are present here |
| `AI_Workflow/` | Agent rules, prompts, setup and checklists | Required before agent work |
| `CHANGELOG.md` | Human-readable change history | Update with verified project changes |

## Naming and output rules
- Use descriptive filenames; avoid ambiguous duplicates and `final-final` variants.
- Each new model should have a folder under `Assets/Models/<ModelName>/` with editable source, export, preview and README.
- Follow `Assets/Textures/TEXTURES/manifest.json` for the imported pack's naming and map conventions; document new assets' dimensions, color space, intended use and license/source.
- For UI, editable Roblox UI instances/scripts are the implementation; reference boards are not full-screen UI textures.
- For scripts, record exact Roblox Explorer path and whether each script is server/client/shared.
- Do not put original/back-up `.rbxl` files into normal Git history casually; decide on binary storage/Git LFS deliberately.