# Roblox Studio import guide

This repository is not a Roblox place file and does not sync itself to Studio. The Luau files in `Assets/Textures/TEXTURES/luau/` are source modules, not a ready-to-open `.rbxl`/`.rbxlx` place.

## Safety first

1. Open a **separate working copy** of the existing place.
2. Do not overwrite `save.rbxl` or `DeepLantern_Backup_Oct09.rbxl`.
3. Do not publish or save over the original place until the import and smoke test have been reviewed.
4. Never put a Roblox API key in the repository or in source code.

## Required Explorer layout for the texture UI modules

Create these instances in `ReplicatedStorage` (instance names and capitalization matter):

```text
ReplicatedStorage
├── Packages
│   └── Fusion                 (compatible Fusion package/module)
└── DeepLantern
    ├── AssetIds               (ModuleScript from luau/AssetIds.luau)
    ├── AtlasData               (ModuleScript from luau/AtlasData.luau)
    ├── DesignTokens            (ModuleScript from luau/DesignTokens.luau)
    ├── Textures                (ModuleScript from luau/Textures.luau)
    └── UI                      (Folder)
        ├── Button              (ModuleScript from luau/UI/Button.luau)
        ├── DiveHUD              (ModuleScript from luau/UI/DiveHUD.luau)
        ├── HullBar              (ModuleScript from luau/UI/HullBar.luau)
        ├── Icon                 (ModuleScript from luau/UI/Icon.luau)
        ├── Panel                (ModuleScript from luau/UI/Panel.luau)
        ├── ResourceBar          (ModuleScript from luau/UI/ResourceBar.luau)
        └── Toast                (ModuleScript from luau/UI/Toast.luau)
```

Install Fusion using a trusted source and choose a version compatible with the API used by these modules. This repository does not currently pin or vendor a Fusion version, so version compatibility must be verified in Studio.

## Texture asset IDs

- `AssetIds.luau` currently has blank IDs for texture entries. UI images and SurfaceAppearance maps that rely on those entries will not display until valid IDs are populated.
- The uploader is experimental and has **not** been validated against a live Roblox Open Cloud account. Start with the credential-free preflight:

  ```bash
  python Assets/Textures/TEXTURES/_generators/upload_assets.py --dry-run
  ```

- A dry run checks local file paths only; it does not test Roblox authentication, permissions, moderation, upload requests, or returned asset IDs.
- If you later perform live uploads, create a narrowly scoped API key in Roblox and keep it in an environment variable or GitHub Actions Secret. Never commit it or paste it into chat.
- Check the returned IDs in Creator Dashboard/Studio and verify each asset is usable by the intended experience.

## Demo smoke test

1. Confirm the Explorer hierarchy above and a compatible Fusion package are present.
2. Copy `luau/UI/DiveHUD.demo.client.luau` into a **LocalScript** under `StarterPlayer/StarterPlayerScripts`.
3. Start a local client test in Studio and inspect **View → Output** for missing modules, asset errors, or Fusion API mismatches.
4. Confirm the HUD renders, battery/depth demo values update, and the scan/recall buttons create toasts.
5. Test at desktop and mobile viewport sizes. This demo is only a UI smoke test; it is not the full game.
6. Remove or disable the demo LocalScript after testing so it does not ship as a production HUD.

## Not yet verified

- Live Open Cloud uploads and moderation status.
- All texture IDs and visual appearance in Studio.
- Fusion version compatibility.
- Full game runtime, client/server behavior, mobile performance, or multiplayer.
- Import of production models or a complete game place; no `.rbxl`/`.rbxlx` file is provided in this repository.
