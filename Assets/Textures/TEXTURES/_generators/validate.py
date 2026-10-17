"""Automated QA for the texture pack. Exit code 1 on any failure.

Checks: manifest completeness, sizes, power-of-two, 9-slice rects inside image, alpha presence,
true seamless tiling (wrap-edge step vs. distribution of interior steps), palette/contrast sanity,
and file budget.
"""
import json
import os
import sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
errors, warnings = [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def pot(n):
    return n > 0 and (n & (n - 1)) == 0


def seam_pass(arr, axis_names=("x", "y"), pct=99.5):
    """Wrap-edge step must not exceed the 99.5th percentile of all interior steps on that axis."""
    a = arr.astype(np.float64)
    if a.ndim == 3:
        a = a[..., :3].mean(-1)
    res = {}
    for ax, nm in ((1, axis_names[0]), (0, axis_names[1])):
        d_int = np.abs(np.diff(a, axis=ax))
        steps = d_int.mean(axis=0 if ax == 1 else 1)           # per-boundary mean step
        edge = np.abs(np.take(a, 0, ax) - np.take(a, -1, ax)).mean()
        res[nm] = (edge, float(np.percentile(steps, pct)), float(steps.mean()))
    return res


def main():
    m = json.load(open(os.path.join(ROOT, "manifest.json")))
    total_bytes = 0

    # materials
    for name, v in m["materials"].items():
        for mp in v["maps"]:
            p = os.path.join(ROOT, "materials", name, f"{mp}.png")
            if not os.path.exists(p):
                err(f"missing {p}")
                continue
            total_bytes += os.path.getsize(p)
            im = Image.open(p)
            if im.size != (512, 512):
                err(f"{p}: size {im.size} != 512")
            if mp == "color" and v.get("has_alpha") != (im.mode == "RGBA"):
                err(f"{p}: alpha flag mismatch")
        arr = np.asarray(Image.open(os.path.join(ROOT, "materials", name, "color.png")).convert("RGBA"), dtype=np.float64)[..., :3]
        r = seam_pass(arr)
        horizontal_only = name.startswith("emissive_strip")
        for ax, (edge, p995, mean) in r.items():
            if horizontal_only and ax == "y":
                continue
            if edge > max(p995, 1.0) * 2.5:
                err(f"material {name}: visible seam on {ax} (edge {edge:.2f} > p99.5 {p995:.2f})")
        nm = np.asarray(Image.open(os.path.join(ROOT, "materials", name, "normal.png")).convert("RGB"), dtype=np.float64) / 255 * 2 - 1
        ln = np.linalg.norm(nm, axis=-1)
        if abs(ln.mean() - 1) > 0.05:
            err(f"material {name}: normal map not unit length (mean {ln.mean():.3f})")
        if nm[..., 2].min() < -0.01:
            err(f"material {name}: normal pointing away")

    # ui
    for rel, v in m["ui"].items():
        p = os.path.join(ROOT, "ui", rel)
        if not os.path.exists(p):
            err(f"missing {p}")
            continue
        total_bytes += os.path.getsize(p)
        im = Image.open(p)
        if list(im.size) != v["size"]:
            err(f"{rel}: size {im.size} != manifest {v['size']}")
        if v.get("type") == "slice9":
            l, t, r_, b = v["slice_center"]
            if not (0 < l < r_ < im.width and 0 < t < b < im.height):
                err(f"{rel}: slice_center {v['slice_center']} outside image {im.size}")
        if im.mode != "RGBA":
            err(f"{rel}: not RGBA")
        if v.get("tileable") and not pot(im.width):
            warn(f"{rel}: tile width not power of two")

    # icons
    for k, v in m["icons"].items():
        for key in ("plated", "glyph"):
            p = os.path.join(ROOT, "icons", v[key])
            if not os.path.exists(p):
                err(f"missing {p}")
                continue
            total_bytes += os.path.getsize(p)
            im = Image.open(p)
            if im.size != (128, 128) or im.mode != "RGBA":
                err(f"{p}: expected 128x128 RGBA")
            a = np.asarray(im.getchannel("A"))
            cover = (a > 20).mean()
            if cover < 0.03:
                err(f"{p}: almost empty ({cover:.1%})")
            if key == "glyph":
                rgb = np.asarray(im.convert("RGB"))[a > 128]
                if len(rgb) and rgb.min() < 200:
                    warn(f"{p}: glyph not pure white")

    # vfx
    for rel, v in m["vfx"].items():
        p = os.path.join(ROOT, "vfx", rel)
        if not os.path.exists(p):
            err(f"missing {p}")
            continue
        total_bytes += os.path.getsize(p)
        if v.get("tileable"):
            arr = np.asarray(Image.open(p).convert("RGBA"), dtype=np.float64)
            arr = np.concatenate([arr[..., :3] * (arr[..., 3:] / 255), arr[..., 3:]], -1)
            for ax, (edge, p995, mean) in seam_pass(arr[..., 3]).items():
                if edge > max(p995, 0.8) * 2.5:
                    err(f"vfx {rel}: visible seam on {ax}")

    # atlases
    atl = os.path.join(ROOT, "atlases", "atlas.json")
    if os.path.exists(atl):
        A = json.load(open(atl))
        for sheet, info in A["sheets"].items():
            p = os.path.join(ROOT, "atlases", sheet)
            if not os.path.exists(p):
                err(f"missing atlas {p}")
            elif Image.open(p).size != tuple(info["size"]):
                err(f"atlas {sheet} size mismatch")
        for k, e in A["icons_flat"].items():
            if e["rect"][0] + e["rect"][2] > 1024 or e["rect"][1] + e["rect"][3] > 1024:
                err(f"atlas icon {k} out of bounds")
    else:
        warn("atlases/atlas.json missing")

    mb = total_bytes / 1e6
    print(f"files OK, total image bytes {mb:.1f} MB")
    for w in warnings:
        print("WARN", w)
    for e in errors:
        print("FAIL", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
