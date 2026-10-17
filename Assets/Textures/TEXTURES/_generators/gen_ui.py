"""Generate UI textures: 9-slice glass panels, bars, buttons, tiles, glows (supersampled)."""
import json
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
from tex_common import *  # noqa

SS = 4
OUT = os.path.join(ROOT, "ui")
MANIFEST = {}


def c4(hexc, a=1.0):
    r, g, b = hex2rgb(PAL.get(hexc, hexc))
    return (r, g, b, int(round(a * 255)))


def poly_pts(w, h, c, inset=0.0):
    i = inset
    p = [(c + i, i), (w - c - i, i), (w - i, c + i), (w - i, h - c - i),
         (w - c - i, h - i), (c + i, h - i), (i, h - c - i), (i, c + i)]
    return [(x * SS, y * SS) for x, y in p]


def gradient_img(w, h, top, bot, at, ab):
    W, H = w * SS, h * SS
    t = np.linspace(0, 1, H)[:, None, None]
    top_c = np.array(hex2rgb(PAL.get(top, top)), dtype=float)
    bot_c = np.array(hex2rgb(PAL.get(bot, bot)), dtype=float)
    rgb = top_c * (1 - t) + bot_c * t
    a = (at * (1 - t) + ab * t) * 255
    arr = np.concatenate([np.broadcast_to(rgb, (H, W, 3)), np.broadcast_to(a, (H, W, 1))], -1)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def shape(w, h, c, top, bot, at, ab, border=None, ba=1.0, bw=1.0, hl=0.0,
          ticks=None, fn_mask=None, inner=None):
    mask = Image.new("L", (w * SS, h * SS), 0)
    if fn_mask:
        fn_mask(ImageDraw.Draw(mask), w, h)
    else:
        ImageDraw.Draw(mask).polygon(poly_pts(w, h, c), fill=255)
    base = gradient_img(w, h, top, bot, at, ab)
    if hl:
        g = np.zeros((h * SS, w * SS, 4), dtype=np.uint8)
        t = np.clip(1 - np.linspace(0, 1, h * SS) / 0.5, 0, 1)[:, None]
        g[..., 0:3] = 255
        g[..., 3] = (t * hl * 255).astype(np.uint8)
        base = Image.alpha_composite(base, Image.fromarray(g, "RGBA"))
    a = np.asarray(base.getchannel("A"), dtype=float) * np.asarray(mask, dtype=float) / 255
    base.putalpha(Image.fromarray(a.astype(np.uint8)))
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    out = Image.alpha_composite(out, base)
    if border:
        lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        pts = poly_pts(w, h, c, inset=bw / 2)
        d.line(pts + [pts[0]], fill=c4(border, ba), width=int(bw * SS), joint="curve")
        out = Image.alpha_composite(out, lay)
    if inner:
        lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        pts = poly_pts(w, h, c, inset=bw + 1.5)
        d.line(pts + [pts[0]], fill=c4(inner[0], inner[1]), width=int(SS * 0.75), joint="curve")
        out = Image.alpha_composite(out, lay)
    if ticks:
        lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        L, m = 9 * SS, 1.5 * SS
        col = c4(ticks, 1.0)
        tw = int(2 * SS)
        # top-left and bottom-right accent ticks
        d.line([(m + c * SS * 0.6, m), (m + c * SS * 0.6 + L, m)], fill=col, width=tw)
        d.line([(m, m + c * SS * 0.6), (m, m + c * SS * 0.6 + L)], fill=col, width=tw)
        W, H = w * SS, h * SS
        d.line([(W - m - c * SS * 0.6, H - m), (W - m - c * SS * 0.6 - L, H - m)], fill=col, width=tw)
        d.line([(W - m, H - m - c * SS * 0.6), (W - m, H - m - c * SS * 0.6 - L)], fill=col, width=tw)
        out = Image.alpha_composite(out, lay)
    return out.resize((w, h), Image.LANCZOS)


def out(rel, img, **meta):
    path = os.path.join(OUT, rel)
    save_img(path, img)
    MANIFEST[rel] = dict(size=list(img.size), **meta)


def sliced(rel, img, rect, note):
    out(rel, img, type="slice9", slice_center=list(rect), usage=note)


# ----------------------------------------------------------------- panels
PANELS = {
    "panel_glass": ("#0d2a52", "#071a35", .82, .88, "#14b8a6", .85, None),
    "panel_glass_dim": ("#08193a", "#050f26", .55, .62, "#14b8a6", .5, None),
    "panel_glass_elevated": ("#14386a", "#0b2549", .90, .94, "#2ad8ff", .95, "#2ad8ff"),
    "panel_glass_solid": ("#0b2447", "#061630", 1.0, 1.0, "#14b8a6", .9, None),
    "panel_glass_alert": ("#3a0d18", "#1d0710", .88, .92, "#ff4d5e", .95, "#ff4d5e"),
    "panel_glass_warning": ("#3a2a08", "#1f1604", .88, .92, "#fbbf24", .95, "#fbbf24"),
    "panel_glass_discovery": ("#2a1458", "#150a30", .88, .92, "#a78bfa", .95, "#a78bfa"),
}


def build_panels():
    for name, (t, b, at, ab, br, ba, tick) in PANELS.items():
        img = shape(64, 64, 7, t, b, at, ab, border=br, ba=ba, bw=1.0, hl=0.07, ticks=tick)
        sliced(f"panels/{name}.png", img, (16, 16, 48, 48),
               "ImageLabel ScaleType=Slice, SliceCenter=Rect(16,16,48,48). Chamfer is baked in: do not add UICorner.")
    toast = shape(64, 32, 6, "#0d2a52", "#071a35", .9, .94, border="#14b8a6", ba=.9, hl=0.07)
    sliced("panels/panel_toast.png", toast, (14, 14, 50, 18), "Toast background (small, auto-dismiss ~3s).")
    outline = shape(64, 64, 7, "#000000", "#000000", 0, 0, border="#2ad8ff", ba=1.0, bw=1.5, ticks="#2ad8ff")
    sliced("panels/frame_select.png", outline, (16, 16, 48, 48), "Selection / gamepad focus frame, transparent fill.")


# ----------------------------------------------------------------- buttons
BUTTON_STYLES = {
    "primary": dict(top="#22c8f5", bot="#0a78b8", border="#9ceeff", at=1, ab=1),
    "secondary": dict(top="#12315c", bot="#0a1f3f", border="#14b8a6", at=.92, ab=.95),
    "danger": dict(top="#c0283a", bot="#6a1020", border="#ff8a94", at=1, ab=1),
}


def shift(hexc, f):
    r, g, b = hex2rgb(PAL.get(hexc, hexc))
    if f >= 0:
        r, g, b = [int(v + (255 - v) * f) for v in (r, g, b)]
    else:
        r, g, b = [int(v * (1 + f)) for v in (r, g, b)]
    return "#%02x%02x%02x" % (r, g, b)


def gray(hexc, mix=0.8):
    r, g, b = hex2rgb(PAL.get(hexc, hexc))
    l = int(0.3 * r + 0.59 * g + 0.11 * b)
    return "#%02x%02x%02x" % tuple(int(v * (1 - mix) + l * mix) for v in (r, g, b))


def build_buttons():
    for style, s in BUTTON_STYLES.items():
        for state in ("default", "hover", "pressed", "disabled", "focus"):
            top, bot, border, at, ab = s["top"], s["bot"], s["border"], s["at"], s["ab"]
            hl, ba = 0.18, 0.95
            ticks = None
            inner = None
            if state == "hover":
                top, bot, border = shift(top, .14), shift(bot, .14), shift(border, .2)
            elif state == "pressed":
                top, bot = shift(bot, -.05), shift(bot, -.3)
                hl = 0.0
            elif state == "disabled":
                top, bot, border = gray(top), gray(bot), gray(border)
                at, ab, ba, hl = at * .45, ab * .45, .4, 0.05
            elif state == "focus":
                inner = ("#2ad8ff", 1.0)
                border = "#2ad8ff"
            img = shape(64, 32, 6, top, bot, at, ab, border=border, ba=ba, bw=1.0 if state != "focus" else 2.0,
                        hl=hl, inner=inner)
            sliced(f"buttons/button_{style}_{state}.png", img, (14, 12, 50, 20),
                   "ImageButton ScaleType=Slice; swap Image per state (default/hover/pressed/disabled/focus). Min hit target 48px.")


# ----------------------------------------------------------------- bars
def pill(w, h, top, bot, at, ab, border=None, ba=1.0, gloss=0.0):
    W, H = w * SS, h * SS
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], radius=H // 2, fill=255)
    base = gradient_img(w, h, top, bot, at, ab)
    if gloss:
        g = np.zeros((H, W, 4), dtype=np.uint8)
        t = np.clip(1 - np.linspace(0, 1, H) / 0.5, 0, 1)[:, None]
        g[..., :3] = 255
        g[..., 3] = (t * gloss * 255).astype(np.uint8)
        base = Image.alpha_composite(base, Image.fromarray(g, "RGBA"))
    a = np.asarray(base.getchannel("A"), dtype=float) * np.asarray(mask, dtype=float) / 255
    base.putalpha(Image.fromarray(a.astype(np.uint8)))
    if border:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle([SS / 2, SS / 2, W - 1 - SS / 2, H - 1 - SS / 2], radius=H // 2,
                                              outline=c4(border, ba), width=SS)
        base = Image.alpha_composite(base, lay)
    return base.resize((w, h), Image.LANCZOS)


BAR_FILLS = {
    "white": ("#ffffff", "#c3d3e6", "Neutral fill, tint with ImageColor3"),
    "aqua": ("#6beaff", "#009fd6", "Battery/Oxygen normal"),
    "amber": ("#ffd166", "#e08a00", "Cargo"),
    "warning": ("#ffe066", "#e0a800", "Battery/Oxygen low reserve (yellow)"),
    "critical": ("#ff7a85", "#d11f32", "Battery/Oxygen critical, hull critical (red)"),
    "purple": ("#c9aaff", "#7040e0", "Research progress"),
}


def build_bars():
    tr = pill(32, 16, "#050e1f", "#0a1a33", .78, .85, border="#14b8a6", ba=.7)
    sliced("bars/bar_track.png", tr, (8, 7, 24, 9), "Bar background. Fill clipped inside with ImageLabel Size scale X.")
    for k, (t, b, note) in BAR_FILLS.items():
        sliced(f"bars/bar_fill_{k}.png", pill(32, 16, t, b, 1, 1, gloss=0.35), (8, 7, 24, 9),
               f"{note}. Pair with bar_track; use ColorBlind-safe icon+text too.")
    for k, (t, b, br) in {"full": ("#8af0ff", "#10a8d8", "#d6faff"), "empty": ("#050e1f", "#0a1a33", "#14b8a6"),
                          "damaged": ("#ff7a85", "#c01a2e", "#ffd0d4")}.items():
        a = 0.8 if k == "empty" else 1
        img = shape(24, 16, 3, t, b, a, a, border=br, ba=.8 if k == "empty" else 1, bw=1.0, hl=0.25 if k != "empty" else 0)
        out(f"bars/hull_segment_{k}.png", img, type="image", usage="One segment of the segmented Hull bar (UIListLayout horizontal).")


# ----------------------------------------------------------------- glows / shadows
def soft_box(color, blur, inset, r, a, size=64):
    W = size * SS
    lay = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([inset * SS, inset * SS, W - inset * SS, W - inset * SS],
                                          radius=r * SS, fill=c4(color, a))
    lay = lay.filter(ImageFilter.GaussianBlur(blur * SS))
    return lay.resize((size, size), Image.LANCZOS)


def build_glows():
    sliced("glow/shadow_soft.png", soft_box("#000000", 6, 20, 6, .7), (28, 28, 36, 36),
           "Soft drop shadow under panels; place behind with larger Size.")
    for k, c in {"aqua": "#00d1ff", "amber": "#f59e0b", "red": "#ef4444", "purple": "#8b5cf6"}.items():
        sliced(f"glow/glow_{k}.png", soft_box(c, 5, 20, 5, .85), (28, 28, 36, 36),
               "Functional glow only (GDD: glow only when functional). Place behind element.")


# ----------------------------------------------------------------- misc
def build_misc():
    # divider
    W, H = 256, 4
    x = np.linspace(-1, 1, W)[None, :]
    a = np.clip(1 - np.abs(x) ** 1.6, 0, 1) * np.ones((H, 1))
    arr = np.zeros((H, W, 4))
    arr[..., :3] = np.array(hex2rgb(PAL["teal"]))
    arr[..., 3] = a * 255 * np.array([0.25, 0.9, 0.9, 0.25])[:, None]
    out("misc/divider_h.png", Image.fromarray(arr.astype(np.uint8), "RGBA"), type="image",
        usage="Horizontal divider with faded ends (use sparingly; prefer whitespace).")
    # scanlines
    sc = np.zeros((4, 8, 4), dtype=np.uint8)
    sc[0, :, :] = (255, 255, 255, 18)
    out("misc/tile_scanlines.png", Image.fromarray(sc, "RGBA"), type="tile", tile_size=[8, 4],
        usage="HUD glass scanline overlay. ScaleType=Tile, TileSize=UDim2.fromOffset(8,4), ImageTransparency ~0.5.")
    # grid tile
    g = np.zeros((32, 32, 4), dtype=np.uint8)
    g[:, :] = (0, 0, 0, 0)
    g[0, :, :] = (20, 184, 166, 70)
    g[:, 0, :] = (20, 184, 166, 70)
    for k in (8, 16, 24):
        g[k, :, :] = (20, 184, 166, 22)
        g[:, k, :] = (20, 184, 166, 22)
    out("misc/tile_grid_32.png", Image.fromarray(g, "RGBA"), type="tile", tile_size=[32, 32],
        usage="Blueprint/terminal background grid.")
    # dots
    d = np.zeros((16, 16, 4), dtype=np.uint8)
    d[8, 8] = (20, 184, 166, 120)
    out("misc/tile_dots_16.png", Image.fromarray(d, "RGBA"), type="tile", tile_size=[16, 16], usage="Dot matrix background.")
    # grain
    n = (rng(7).random((128, 128)) * 255).astype(np.uint8)
    arr = np.dstack([np.full((128, 128), 255, np.uint8)] * 3 + [(n * 0.09).astype(np.uint8)])
    out("misc/tile_grain_128.png", Image.fromarray(arr, "RGBA"), type="tile", tile_size=[128, 128],
        usage="Subtle film grain over panels (optional).")
    # scrollbar
    out("misc/scroll_thumb.png", pill(16, 32, "#4ee0ff", "#0c9bc9", .8, .8, gloss=0.2), type="slice9",
        slice_center=[7, 8, 9, 24], usage="ScrollingFrame.ScrollBarImageColor3 neutral; use as ScrollBar image.")
    # checkbox
    for state, fill_a, mark in (("off", .6, False), ("on", .9, True)):
        img = shape(32, 32, 5, "#0d2a52", "#071a35", fill_a, fill_a, border="#14b8a6" if not mark else "#2ad8ff", ba=1, bw=1.5)
        if mark:
            S4 = 4
            big = img.resize((128, 128), Image.LANCZOS)
            dr = ImageDraw.Draw(big)
            dr.line([(34, 66), (56, 90), (96, 40)], fill=c4("#2ad8ff"), width=12, joint="curve")
            img = big.resize((32, 32), Image.LANCZOS)
        out(f"misc/checkbox_{state}.png", img, type="image", usage="Checkbox (icon + text for state; not colour only).")
    # slider thumb
    big = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    dr = ImageDraw.Draw(big)
    dr.ellipse([12, 12, 116, 116], fill=c4("#2ad8ff", .25))
    dr.ellipse([30, 30, 98, 98], fill=c4("#6beaff"), outline=c4("#d6faff"), width=6)
    out("misc/slider_thumb.png", big.resize((32, 32), Image.LANCZOS), type="image", usage="Slider thumb (settings).")
    # notification dot
    big = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    dr = ImageDraw.Draw(big)
    dr.ellipse([6, 6, 58, 58], fill=c4("#ef4444"), outline=c4("#ffd0d4"), width=4)
    out("misc/badge_dot.png", big.resize((16, 16), Image.LANCZOS), type="image", usage="Unread / new-codex-entry dot.")


def build_all():
    build_panels()
    build_buttons()
    build_bars()
    build_glows()
    build_misc()
    with open(os.path.join(OUT, "_report.json"), "w") as f:
        json.dump(MANIFEST, f, indent=1)
    print(len(MANIFEST), "ui textures")


if __name__ == "__main__":
    build_all()
