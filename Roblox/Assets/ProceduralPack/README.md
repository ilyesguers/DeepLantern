# Deep Lantern — Free Modular Asset Pack (starter)

This is a **safe, free starter pack** combining procedural Roblox parts with a planned slot for a few AI-generated hero meshes. It is not yet a finished/imported production asset library.

## What is included now
- `ResearchConsole`: modular station console with cyan/teal display and amber status light.
- `DiveBeacon`: simple dive navigation marker with a cyan light.
- `SampleCanister`: collectible/research prop.
- `KelpCoral_Cluster_*`: deterministic procedural coral clusters with variation.
- A Studio Command Bar preview script that creates everything inside one new folder.

These are built from native Roblox Parts and materials; there are no external model downloads, API keys, or paid services required for the preview.

## Safe preview
1. Open a **separate test place**, not the original `save.rbxl` and not `DeepLantern_Backup_Oct09.rbxl`.
2. Open `Roblox/Assets/ProceduralPack/BuildPreview.server.lua`.
3. Copy its contents into Studio's Command Bar and run once.
4. Inspect `Workspace.DeepLantern_AssetPack_Preview`.
5. Delete that one folder to roll back. The script refuses to overwrite an existing folder with that name.

## Important limitations
- This script has not been run in Roblox Studio from this repository environment.
- This is a visual blockout/preview, not a final art pass. Check scale, collision, lighting and mobile performance in Studio.
- The generated display is decorative; it has no gameplay logic or interactions.
- Do not copy the preview directly into the live place before review.
- AI-generated FBX/GLB models should be added only after checking download rights, textures, triangle count, pivots, scale and import behavior. Keep source files and license/provenance notes beside each model.
- Prefer MeshParts with textures for hero assets and native Parts for simple modular geometry. Reuse variations instead of generating dozens of nearly identical meshes.

## Next safe stage
Inspect the live Studio hierarchy with Claude first, then compare this pack against existing props. Keep only the missing assets and adjust their dimensions to match the game.
