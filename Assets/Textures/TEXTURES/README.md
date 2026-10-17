# Deep Lantern — Texture Pack (AI-ready)

496 PNG files (+ Luau UI components and tooling) generated procedurally in the Deep Lantern art direction. Read this file first, then `manifest.json`.

**Source of truth:** GDD Parts 1–10. These textures define *look only*. Never derive gameplay values, prices, depths or mechanics from them.

## Style rules (from the GDD and the visual references)
- Palette: deep navy `#081E3B`, aqua `#00D1FF`, teal `#14B8A6`, purple `#8B5CF6` (Twilight Reef), amber `#F59E0B`, white `#E6F1FF`, crimson `#EF4444` for alerts.
- UI: semi-transparent glass panels, 1px teal border, chamfered corners, glow only when functional.
- Never use colour alone for state: pair every colour with an icon and text.
- No full-screen white flashes, no strobe. Toasts last ~3s. Non-essential HUD dims after ~5s.
- Performance: event-driven, no per-frame UI polling, respect the particle budgets in GDD Part 10.

## Layout
| Folder | Content | Count |
|---|---|---|
| `materials/<name>/` | 512px tileable PBR: `color`, `normal`, `roughness`, `metalness`, optional `emissive` | 39 sets |
| `ui/panels, buttons, bars, glow, misc` | 9-slice glass UI, button states, bars, glows, tiles | 49 |
| `icons/<category>/` | 128px colour icons, lit and shaded, on a glass plate | 111 |
| `icons/glyph/<category>/` | same icons as white silhouettes (tint with `ImageColor3`) | 111 |
| `atlases/` | 4 x 1024px icon atlases + `atlas.json` (rect per icon) | 4 |
| `vfx/particles, beams, hud, backdrops` | particles, beams, sonar, scanner, vignettes, zone gradients | 29 |
| `branding/` | wordmark logo, game icon 512/128, loading backdrop 1920x1080, station label decals | 15 |
| `previews/` | contact sheets of everything (open these first) | 5 |
| `luau/` | `DesignTokens`, `Textures`, `AssetIds`, `AtlasData`, `stylua.toml` | 5 |
| `luau/UI/` | Fusion 0.3 components: `Panel`, `Button`, `Icon`, `ResourceBar`, `HullBar`, `Toast`, `DiveHUD` + demo | 8 |
| `_generators/` | Python that regenerates everything, `validate.py` (QA), `upload_assets.py` | — |

## How to use (Roblox)
1. Upload the PNGs (Studio Asset Manager or Open Cloud), then paste the ids into `luau/AssetIds.luau`.
2. UI: build with the Fusion components in `luau/UI` (`Panel`, `Button`, `ResourceBar`, `HullBar`, `Toast`, `DiveHUD`). Raw use: `Textures.applySlice(imageLabel, DesignTokens.slices.panel)`. Do not add `UICorner`; the chamfer is baked in.
   Place `luau/` as `ReplicatedStorage.DeepLantern` (so `DeepLantern.UI`, `DeepLantern.Textures`, ...) and Fusion at `ReplicatedStorage.Packages.Fusion`.
3. Buttons: swap `Image` per state `default / hover / pressed / disabled / focus`. Hit target at least 48px.
4. Bars: `bar_track` behind, `bar_fill_*` clipped on top. Battery/Oxygen uses `aqua` → `warning` → `critical`. Hull uses `hull_segment_*` in a horizontal `UIListLayout`.
5. Icons: use the `Icon` component or `Textures.atlasIcon(key, glyph)` (atlas = 4 uploads instead of 222). `Textures.icon/glyph` return single files.
6. World parts: `Textures.surfaceAppearance("hull_white")` on a MeshPart, or `color.png` on a `Texture` with `StudsPerTileU/V = studs_per_tile` from the manifest.
7. Emissive maps: use on Neon-style overlays; crystals, strips, runes and bioluminescence rely on them for the Twilight Reef look.

## Which material where
- Shallows: `sand_seabed`, `rock_dark`, `coral_pink`, `rusted_metal` (wrecks), `caustics_tile` (vfx).
- Kelp Forest: `kelp_green`, `rock_mossy`, `moss`, `light_rays_tile`.
- Twilight Reef: `coral_purple`, `crystal_purple`, `crystal_blue`, `bio_skin_*`.
- Station: `station_wall`, `station_floor`, `glass_blue`, `emissive_strip_*`, `hull_*`.
- Submarines: `hull_white` (default), `hull_ocean_blue`, `hull_deep_black`, `hull_sand`, `hull_arctic`, `hull_camo`, plus `carbon_composite`, `rubber_seal`.
- Creature variants: `scales_normal / bioluminescent / albino / armored / corrupted / rare`.
- Relics: `relic_stone`, `relic_obsidian`.

## Icon categories
`hud`, `roles`, `resources`, `anomalies`, `equipment`, `codex`, `creatures`, `zones`, `wings`, `classes`, `tiers`. Post-MVP items (Abyss, Lost Ruins, The Hollow, Beyond, Citadel, Deep Empire, Multi-Crew) are drawn greyed or locked; keep them hidden in MVP UI.

## Rules for AI agents
- Reuse existing textures and tokens; do not invent new colours or inline `Color3` at call sites.
- Do not add UI for systems the GDD forbids (minimap, GPS markers, fast travel, loot boxes, a third currency).
- To add a texture: extend the matching `_generators/gen_*.py`, run it, then `python3 _generators/build_manifest.py`.
- Regenerate all: `cd TEXTURES/_generators && for g in gen_materials gen_ui gen_icons gen_vfx build_manifest; do python3 $g.py; done` (needs numpy, scipy, Pillow).

## Quality gates
- `python3 _generators/validate.py` checks sizes, 9-slice rects, normal-map unit length, true seamlessness (calibrated and proven to flag a deliberately broken tile), atlas bounds and manifest completeness. It must report 0 errors before committing.
- Luau files have been checked for balanced syntax only. They have **not** been run in Studio: test `DiveHUD.demo.client.luau` first and fix any Fusion API drift.
- `upload_assets.py` is written from the public Open Cloud docs and has not been run against the live API; use `--dry-run` first.

## Known limits
- Procedural art, not hand-painted: good as a consistent base layer. Hero assets (key art, logo, creature models) still need an artist or an image model.
- No fonts and no audio included. The logo uses Poppins Bold / Inter (open fonts); in-game text should use the `BuilderSans` / `RobotoMono` tokens.
- Battery/Oxygen warning thresholds (30% / 15%) in `ResourceBar.batteryStyle` are placeholders: the GDD defers exact numbers to balancing.
- Ids in `AssetIds.luau` are empty until you upload.
