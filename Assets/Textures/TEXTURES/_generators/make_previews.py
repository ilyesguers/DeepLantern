"""Contact sheets so the pack can be reviewed on GitHub without opening 500 files."""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "previews")
os.makedirs(OUT, exist_ok=True)
BG = (10, 22, 44, 255)
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)


def sheet(items, cols, cell, label_h=16, name="x"):
    rows = (len(items) + cols - 1) // cols
    img = Image.new("RGBA", (cols * cell, rows * (cell + label_h)), BG)
    d = ImageDraw.Draw(img)
    for i, (lab, path) in enumerate(items):
        im = Image.open(path).convert("RGBA")
        sc = min((cell - 8) / im.width, (cell - 8) / im.height)
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        x, y = (i % cols) * cell, (i // cols) * (cell + label_h)
        img.alpha_composite(im, (x + (cell - im.width) // 2, y + 4))
        d.text((x + 4, y + cell - 2), lab[:cell // 7], fill=(160, 200, 230), font=F)
    img.convert("RGB").save(os.path.join(OUT, name + ".png"), optimize=True)


def main():
    m = json.load(open(os.path.join(ROOT, "manifest.json")))
    sheet([(n, f"{ROOT}/materials/{n}/color.png") for n in sorted(m["materials"])], 8, 180, name="materials")
    sheet([(k, f"{ROOT}/icons/{v['plated']}") for k, v in sorted(m["icons"].items())], 12, 120, name="icons")
    sheet([(k.split('/')[-1], f"{ROOT}/ui/{k}") for k in sorted(m["ui"]) if not k.startswith("misc/tile")], 8, 140, name="ui")
    sheet([(k.split('/')[-1], f"{ROOT}/vfx/{k}") for k in sorted(m["vfx"])], 6, 220, name="vfx")
    sheet([(k, f"{ROOT}/branding/{k}") for k in sorted(m["branding"])], 4, 300, name="branding")
    print("previews written")


if __name__ == "__main__":
    main()
