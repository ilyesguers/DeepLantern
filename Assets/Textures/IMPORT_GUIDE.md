# Texture pack integration guide

The reviewed texture archive contains a self-contained `TEXTURES/` tree with material maps, UI/icon/branding/VFX resources, Luau helpers, generator scripts, reports, and `manifest.json`.

## Required layout

Keep source archive paths intact initially, for example:

- `TEXTURES/materials/<material>/{color,normal,roughness,metalness,emissive}.png`
- `TEXTURES/atlases/`
- `TEXTURES/icons/`
- `TEXTURES/branding/`
- `TEXTURES/vfx/`
- `TEXTURES/luau/`
- `TEXTURES/_generators/`
- `TEXTURES/manifest.json`

Do not move files into production folders until the manifest paths and every script reference have been updated together.

## Before using in Roblox

1. Run `TEXTURES/_generators/validate.py` from the extracted package root and retain its report.
2. Check image dimensions, color-space assumptions, normal-map conventions, tiling/UV assumptions, and licensing/provenance.
3. Confirm the project’s UI dependency setup; the pack's UI modules expect Fusion 0.3.
4. Upload assets only through an approved workflow. Do not commit credentials or run the uploader automatically.
5. Replace placeholders in `TEXTURES/luau/AssetIds.luau` only with verified Roblox asset IDs.
6. Test imports and UI in a separately named working place on desktop and mobile.

The archive's automated validation result was 0 errors and 0 warnings, and the 11 Python files passed syntax compilation. These checks do not prove that Roblox Studio can import every asset or that the Luau modules run in the current game.
