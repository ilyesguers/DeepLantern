"""Merge all generator reports into TEXTURES/manifest.json and emit AssetIds.luau (placeholder map)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from tex_common import ROOT, PAL  # noqa

STUDS = {}


def load(p):
    with open(os.path.join(ROOT, p)) as f:
        return json.load(f)


def main():
    mats = load("materials/_report.json")
    ui = load("ui/_report.json")
    icons = load("icons/_report.json")
    vfx = load("vfx/_report.json")
    brand = load("branding/_report.json")
    atlas = load("atlases/atlas.json")

    manifest = {
        "name": "Deep Lantern texture pack",
        "version": "1.0.0",
        "source_of_truth": "GDD Parts 1-10 (visual references are style only; no gameplay values come from images)",
        "palette": PAL,
        "conventions": {
            "materials": {
                "size": 512, "tileable": True,
                "maps": {"color.png": "BrickColor/ColorMap (sRGB, alpha only for glass)", "normal.png": "NormalMap OpenGL +Y up (Roblox compatible)",
                         "roughness.png": "RoughnessMap (white=rough)", "metalness.png": "MetalnessMap (white=metal)",
                         "emissive.png": "optional; apply as Neon/emissive overlay or SurfaceAppearance.EmissiveMaskContent"},
                "roblox": "Upload color/normal/roughness/metalness as Images, then use SurfaceAppearance on a MeshPart. For plain Parts use color.png on a Texture (StudsPerTileU/V = studs_per_tile).",
            },
            "ui_panels": "9-slice. ImageLabel.ScaleType = Slice, SliceCenter from manifest (px in source). Chamfer is baked in, do not add UICorner.",
            "icons": {"size": 128, "plated": "colour icon on glass plate", "glyph": "white silhouette, tint with ImageColor3"},
            "vfx": "Particles: ParticleEmitter.Texture. Beams: Beam.Texture. Respect GDD budgets (<=150 particles Low).",
        },
        "materials": mats,
        "ui": ui,
        "icons": icons,
        "vfx": vfx,
        "branding": brand,
        "atlases": {"cell": atlas["cell"], "sheets": atlas["sheets"], "data_module": "luau/AtlasData.luau"},
    }
    with open(os.path.join(ROOT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)

    # AssetIds.luau: file path -> "" so the AI/dev fills rbxassetid after upload.
    lines = ["--!strict", "-- Fill each value with the rbxassetid://<id> after uploading the PNG. Keys are repo-relative paths.",
             "-- Code must go through Textures.get(key) so a missing id degrades gracefully.", "local ids: { [string]: string } = {"]
    def add(prefix, items):
        for k in sorted(items):
            lines.append(f'\t["{prefix}{k}"] = "",')
    for name, m in sorted(mats.items()):
        for mp in m["maps"]:
            lines.append(f'\t["materials/{name}/{mp}.png"] = "",')
    add("ui/", ui)
    for k in sorted(icons):
        lines.append(f'\t["icons/{k}.png"] = "",')
        lines.append(f'\t["icons/glyph/{k}.png"] = "",')
    add("vfx/", vfx)
    add("branding/", brand)
    for sh in sorted(atlas["sheets"]):
        lines.append(f'\t["atlases/{sh}"] = "",')
    lines += ["}", "", "return table.freeze(ids)", ""]
    with open(os.path.join(ROOT, "luau", "AssetIds.luau"), "w") as f:
        f.write("\n".join(lines))
    n = sum(len(m["maps"]) for m in mats.values()) + len(ui) + 2 * len(icons) + len(vfx) + len(brand) + len(atlas["sheets"])
    print("manifest ok;", len(mats), "materials,", len(ui), "ui,", len(icons), "icons x2,", len(vfx), "vfx =", n, "files")


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "luau"), exist_ok=True)
    main()
