# DeepLantern import review

This folder documents the reviewed source archives and the safe integration plan. It does not replace the approved GDD or the live Roblox place.

## Reviewed source archives

1. `DeepLantern_AI_Programmer_Pack_v2.zip`
   - 33 entries; 23,982,091 uncompressed bytes.
   - Contains the approved GDD in TXT/RTF formats, the original project-state RTF, visual reference boards, and supporting project documentation.
2. `DeepLantern_Textures(1).zip`
   - 612 archive entries: 529 files and 83 directories; 26,508,303 uncompressed bytes.
   - Contains 496 PNG images, 12 Luau files, 11 Python generator/utility files, JSON manifests/reports, and documentation.
   - Reported validator result: 0 errors and 0 warnings. Python syntax checks passed for the 11 Python files. This is not a Roblox Studio runtime test.

## Integration rules

- Merge by path and review differences first; do not blindly extract either archive over the repository root.
- Keep the original approved GDD Parts 1–10 as the design source of truth. The summary is only an index.
- Keep visual references under `Art/VisualReference/`; they are not production models or textures.
- Keep texture source maps and generated UI resources under a clearly named texture asset directory. Preserve the archive's internal `TEXTURES/` hierarchy until integration paths are deliberately approved.
- Confirm the existing UI framework and dependency versions before using the Fusion-based UI components.
- Replace placeholder asset IDs only after the corresponding images are uploaded and tested in Roblox.
- Do not run the Roblox asset uploader without explicit confirmation, valid credentials, and an asset-by-asset review.
- Never overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`. Use a separate working copy and do not save/publish without explicit approval.

## What this branch does not claim

The binary PNG assets and all source archive contents have not yet been committed to this repository by this documentation change. Roblox Studio imports and runtime behavior have not been tested here. See the accompanying import guides for the remaining steps.
