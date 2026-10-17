"""Brand assets for Deep Lantern: wordmark, game icon, loading backdrop, station label decals.

Original artwork (lantern emblem drawn from scratch to match the project's own style guide).
"""
import json
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
from scipy.ndimage import gaussian_filter, minimum_filter

sys.path.insert(0, os.path.dirname(__file__))
from tex_common import *  # noqa

OUT = os.path.join(ROOT, "branding")
REPORT = {}
FONT_BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FONT_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SS = 2


def put(rel, img, **meta):
    save_img(os.path.join(OUT, rel), img)
    REPORT[rel] = dict(size=list(img.size), **meta)


def rgba(h, a=255):
    r, g, b = hex2rgb(PAL.get(h, h))
    return (r, g, b, a)


def shade(img, ss):
    a = np.asarray(img, dtype=np.float64) / 255
    al = a[..., 3]
    hgt = gaussian_filter(al, 2.6 * ss)
    gy, gx = np.gradient(hgt)
    s = (gx + gy) / math.sqrt(2)
    sc = np.percentile(np.abs(s[al > .5]), 98) if (al > .5).any() else 1
    s = np.clip(s / max(sc, 1e-9), -1, 1)
    yy = np.linspace(0, 1, al.shape[0])[:, None]
    rgb = a[..., :3] * (1.1 - 0.24 * yy)[..., None]
    rgb = rgb * (1 + 0.32 * s[..., None]) + np.clip(s, 0, 1)[..., None] * 0.12
    band = al - minimum_filter(al, size=max(2, int(1.8 * ss)))
    rgb *= (1 - 0.35 * np.clip(band, 0, 1))[..., None]
    return Image.fromarray((np.dstack([np.clip(rgb, 0, 1), al]) * 255 + .5).astype(np.uint8), "RGBA")


def lantern(size, glow=True):
    """Original lantern emblem on a transparent square canvas."""
    W = size * SS
    u = lambda v: v * W / 100.0
    L = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    d.arc([u(33), u(4), u(67), u(40)], 190, 350, fill=rgba("#cbd5e1"), width=int(u(3.2)))     # handle
    d.polygon([(u(35), u(28)), (u(65), u(28)), (u(72), u(38)), (u(28), u(38))], fill=rgba("#fbbf24"))   # cap
    d.rounded_rectangle([u(29), u(37), u(71), u(80)], radius=u(8), fill=rgba("#1b3c6e"))               # frame
    d.rounded_rectangle([u(34), u(41), u(66), u(76)], radius=u(6), fill=rgba("#bff3ff"))               # glass
    d.ellipse([u(40), u(50), u(60), u(72)], fill=rgba("#fff7d6"))                                       # flame body
    d.polygon([(u(50), u(44)), (u(56), u(56)), (u(44), u(56))], fill=rgba("#fff7d6"))
    d.rounded_rectangle([u(30), u(78), u(70), u(88)], radius=u(4), fill=rgba("#fbbf24"))               # base
    for x in (42, 50, 58):
        d.line([(u(x), u(41)), (u(x), u(76))], fill=rgba("#1b3c6e"), width=int(u(1.6)))
    L = shade(L, SS)
    if not glow:
        return L.resize((size, size), Image.LANCZOS)
    g = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([u(18), u(34), u(82), u(98)], fill=rgba("#7ff0ff", 120))
    gd.ellipse([u(34), u(48), u(66), u(80)], fill=rgba("#fff2b0", 170))
    g = g.filter(ImageFilter.GaussianBlur(u(7)))
    out = Image.alpha_composite(g, L)
    return out.resize((size, size), Image.LANCZOS)


def tight(img, h):
    bb = img.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
    im = img.crop(bb)
    return im.resize((max(1, int(im.width * h / im.height)), h), Image.LANCZOS)


def spaced_text(txt, font, spacing, W=None):
    """Return an L mask with tracked-out text."""
    widths = [font.getlength(c) for c in txt]
    total = int(sum(widths) + spacing * (len(txt) - 1)) + 8
    asc, desc = font.getmetrics()
    m = Image.new("L", (W or total, asc + desc + 8), 0)
    d = ImageDraw.Draw(m)
    x = 4 if W is None else (W - total) // 2 + 4
    for c, w in zip(txt, widths):
        d.text((x, 4), c, font=font, fill=255)
        x += w + spacing
    return m


def gradient_fill(mask, top, bot):
    w, h = mask.size
    t = np.linspace(0, 1, h)[:, None, None]
    a, b = np.array(hex2rgb(PAL.get(top, top)), float), np.array(hex2rgb(PAL.get(bot, bot)), float)
    rgb = np.broadcast_to(a * (1 - t) + b * t, (h, w, 3))
    img = Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
    img.putalpha(mask)
    return img


def wordmark():
    W, H = 1600, 720
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lan = tight(lantern(900), 330)
    img.alpha_composite(lan, ((W - lan.width) // 2, 10))
    f1 = ImageFont.truetype(FONT_BOLD, 150)
    m1 = spaced_text("DEEP", f1, 34)
    m2 = spaced_text("LANTERN", f1, 20)
    for i, (m, y) in enumerate(((m1, 255), (m2, 255))):
        pass
    # single line "DEEP LANTERN"
    m = spaced_text("DEEP LANTERN", f1, 26)
    scale = min(1.0, (W - 80) / m.width)
    if scale < 1:
        m = m.resize((int(m.width * scale), int(m.height * scale)), Image.LANCZOS)
    x = (W - m.width) // 2
    y = 370
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gm = Image.new("L", (W, H), 0)
    gm.paste(m, (x, y))
    glow_l = Image.new("RGBA", (W, H), rgba("#00d1ff", 255))
    glow_l.putalpha(gm.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.8)))
    img = Image.alpha_composite(img, glow_l)
    shadow = Image.new("RGBA", (W, H), rgba("#020a1c", 220))
    shadow.putalpha(ImageChops.offset(gm, 0, 6).filter(ImageFilter.GaussianBlur(3)))
    img = Image.alpha_composite(img, shadow)
    txt = gradient_fill(gm, "#ffffff", "#7fe9ff")
    img = Image.alpha_composite(img, txt)
    f2 = ImageFont.truetype(FONT_SEMI, 44)
    tm = spaced_text("LIGHT THE WAY DOWN", f2, 22)
    tx = Image.new("L", (W, H), 0)
    tx.paste(tm, ((W - tm.width) // 2, 370 + 185))
    img = Image.alpha_composite(img, gradient_fill(tx, "#6beaff", "#14b8a6").point(lambda v: v) if False else gradient_fill(tx, "#9ceeff", "#14b8a6"))
    bbox = img.getchannel("A").point(lambda v: 255 if v > 4 else 0).getbbox()
    img = img.crop((max(0, bbox[0] - 20), max(0, bbox[1] - 20), min(W, bbox[2] + 20), min(H, bbox[3] + 20)))
    put("logo_wordmark.png", img, usage="Main logo (transparent). Loading screen, title, store header.")


def game_icon():
    N = 512
    y, x = np.mgrid[0:N, 0:N]
    r = np.hypot(x - N / 2, y - N * 0.42) / (N * 0.75)
    bg = ramp(np.clip(r, 0, 1), [(0, "#14508f"), (0.5, "#0a2a55"), (1, "#030c1e")])
    img = to_img(np.dstack([bg, np.ones((N, N))])).convert("RGBA")
    # light rays from above
    rays = np.zeros((N, N))
    for k, a0 in enumerate(np.linspace(-0.55, 0.55, 9)):
        ang = np.arctan2(x - N / 2, y + N * 0.2)
        rays += np.exp(-((ang - a0) / 0.035) ** 2) * (0.4 + 0.6 * ((k * 37) % 7) / 7)
    rays = gaussian_filter(rays, 3) * np.clip(1 - y / (N * 0.9), 0, 1)
    ray = Image.new("RGBA", (N, N), rgba("#8fe6ff", 255))
    ray.putalpha(Image.fromarray((np.clip(rays, 0, 1) * 70).astype(np.uint8)))
    img = Image.alpha_composite(img, ray)
    # bubbles
    rr = rng(11)
    bub = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bub)
    for _ in range(26):
        cx, cy, rad = rr.random() * N, rr.random() * N, 2 + rr.random() * 7
        bd.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(190, 235, 255, int(60 + 100 * rr.random())), width=2)
    img = Image.alpha_composite(img, bub)
    lan = tight(lantern(900), 380)
    img.alpha_composite(lan, ((N - lan.width) // 2, 66))
    # rounded mask + border
    m = Image.new("L", (N * 2, N * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, N * 2 - 1, N * 2 - 1], radius=N * 0.2, fill=255)
    m = m.resize((N, N), Image.LANCZOS)
    img.putalpha(ImageChops.multiply(img.getchannel("A"), m))
    bd = Image.new("RGBA", (N * 2, N * 2), (0, 0, 0, 0))
    ImageDraw.Draw(bd).rounded_rectangle([4, 4, N * 2 - 5, N * 2 - 5], radius=N * 0.2, outline=rgba("#2ad8ff", 230), width=8)
    img = Image.alpha_composite(img, bd.resize((N, N), Image.LANCZOS))
    put("game_icon_512.png", img, usage="Experience icon (Roblox asks for 512x512). Upload as the game icon; no text, readable at 64px.")
    put("game_icon_128.png", img.resize((128, 128), Image.LANCZOS), usage="Small UI use / favicon style.")


def loading_backdrop():
    W, H = 1920, 1080
    y, x = np.mgrid[0:H, 0:W]
    t = y / H
    col = ramp(t, [(0, "#0e6fae"), (0.35, "#0a3d75"), (0.7, "#061f45"), (1, "#020a1a")])
    # god rays
    rays = np.zeros((H, W))
    rr = rng(21)
    for _ in range(14):
        x0 = rr.random() * W * 1.2 - 0.1 * W
        sl = 0.25 + 0.2 * rr.random()
        wd = 30 + rr.random() * 90
        d = (x - (x0 + sl * y)) / wd
        rays += np.exp(-d ** 2) * (0.4 + 0.6 * rr.random())
    rays = gaussian_filter(rays, 6) * (1 - t) ** 1.4
    col = col + rays[..., None] * np.array(rgb01("#7fe0ff")) * 0.22
    # silhouette ridges
    for k, (base, amp, shade_c, seed) in enumerate(((0.80, 70, "#06162f", 1), (0.88, 55, "#040e22", 2), (0.95, 40, "#020814", 3))):
        n = gaussian_filter(rng(seed).standard_normal(W * 2), 60)
        n = (n - n.mean()) / n.std()
        ridge = (base + n[:W] * amp / H)
        m = (t > ridge[None, :]).astype(float)
        m = gaussian_filter(m, 1.2)
        col = col * (1 - m[..., None]) + np.array(rgb01(shade_c)) * m[..., None]
    # vignette
    v = np.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2))
    col *= (1 - 0.45 * smoothstep(0.55, 1.35, v))[..., None]
    img = to_img(col).convert("RGBA")
    snow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(snow)
    for _ in range(420):
        cx, cy, rad = rr.random() * W, rr.random() * H, 0.8 + rr.random() * 2.4
        sd.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(214, 236, 255, int(40 + 140 * rr.random())))
    img = Image.alpha_composite(img, snow.filter(ImageFilter.GaussianBlur(0.8)))
    put("loading_backdrop_1920x1080.png", img.convert("RGB").convert("RGBA"), usage="Loading / title backdrop (no text). Place the wordmark on top, centred.")


def decals():
    """Station label decals: transparent glyph plates with monospace text (SurfaceGui/Decal)."""
    labels = ["POWER CORE", "SUB DOCK", "WORKSHOP", "RESEARCH LAB", "OBSERVATORY", "AQUARIUM", "ARCHIVE", "DOCKING RING", "AIRLOCK", "DEPTH GAUGE"]
    f = ImageFont.truetype(FONT_MONO, 64)
    for lab in labels:
        W, H = 1024, 192
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([4, 4, W - 5, H - 5], radius=26, fill=rgba("#06142c", 235), outline=rgba("#14b8a6", 255), width=4)
        d.rectangle([28, 28, 44, H - 29], fill=rgba("#f59e0b"))
        d.text((74, H / 2), lab, font=f, fill=rgba("#e6f1ff"), anchor="lm")
        for i in range(5):
            d.rectangle([W - 160 + i * 26, 60, W - 160 + i * 26 + 14, H - 61], fill=rgba("#14b8a6", 80 + 35 * i))
        put(f"decals/label_{lab.lower().replace(' ', '_')}.png", img, usage="Station signage. SurfaceGui ImageLabel or Decal on a flat part; matches GDD terminals.")
    # hazard stripe tile
    N = 128
    y, x = np.mgrid[0:N, 0:N]
    st = (((x + y) // 16) % 2).astype(float)
    arr = np.dstack([np.where(st > 0, 0.96, 0.08), np.where(st > 0, 0.62, 0.09), np.where(st > 0, 0.04, 0.10), np.ones((N, N))])
    put("decals/hazard_stripes_tile.png", to_img(arr).convert("RGBA"), tileable=True, usage="Hazard / docking edge stripes (tile, 128px).")


def build_all():
    wordmark()
    game_icon()
    loading_backdrop()
    decals()
    with open(os.path.join(OUT, "_report.json"), "w") as f:
        json.dump(REPORT, f, indent=1)
    print(len(REPORT), "branding assets")


if __name__ == "__main__":
    build_all()
