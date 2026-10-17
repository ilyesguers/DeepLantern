"""Generate tileable PBR material sets (color / normal / roughness / metalness / emissive)."""
import json
import os
import sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from tex_common import *  # noqa
from scipy.ndimage import gaussian_filter

S = 512
OUT = os.path.join(ROOT, "materials")
GRID = np.mgrid[0:S, 0:S]
Y, X = GRID


def M(color, rough, metal, height, nstr=4.0, emissive=None, alpha=None):
    return dict(color=color, rough=np.broadcast_to(rough, (S, S)).copy(),
                metal=np.broadcast_to(metal, (S, S)).copy(), height=height,
                nstr=nstr, emissive=emissive, alpha=alpha)


# ---------------------------------------------------------------- terrain
def rock_dark():
    h = fbm(S, 1, 48, 6)
    r = ridged(fbm(S, 2, 40, 4))
    height = 0.6 * h + 0.4 * r
    col = ramp(height, [(0, "#0d1522"), (0.5, "#2a3a52"), (1, "#5c6f8a")])
    f1, f2, _ = worley(S, 70, 3)
    crack = smoothstep(0, 5, f2 - f1)
    col *= (0.5 + 0.5 * crack)[..., None]
    return M(col, 0.85 + 0.1 * h, 0.0, height * 0.7 + 0.3 * crack, 7)


def rock_mossy():
    base = rock_dark()
    moss = smoothstep(0.52, 0.7, fbm(S, 11, 30, 5))
    mc = ramp(fbm(S, 12, 6, 3), [(0, "#24491f"), (1, "#79ab45")])
    col = base["color"] * (1 - moss[..., None]) + mc * moss[..., None]
    return M(col, 0.9, 0.0, base["height"] + moss * 0.15, 6)


def sand_seabed():
    warp = fbm(S, 21, 60, 3)
    rip = 0.5 + 0.5 * np.sin(2 * np.pi * (10 * Y / S + 0.9 * (warp - 0.5)))
    grain = noise(S, 0.8, 22)
    height = 0.7 * rip + 0.3 * grain
    col = ramp(0.55 * rip + 0.45 * fbm(S, 23, 20, 4), [(0, "#a08f66"), (0.5, "#cdbd92"), (1, "#eadfba")])
    col *= (0.93 + 0.14 * grain)[..., None]
    return M(col, 1.0, 0.0, height, 3)


def coral(cols, emissive_strength=0.0, seed=31, npts=140):
    f1, f2, ids = worley(S, npts, seed)
    bump = 1 - np.clip(f1 / 30, 0, 1)
    palette = np.array([rgb01(c) for c in cols])
    base = palette[ids % len(palette)]
    n = fbm(S, seed + 1, 8, 3)
    col = base * (0.45 + 0.65 * bump)[..., None] * (0.9 + 0.2 * n)[..., None]
    em = None
    if emissive_strength:
        em = np.clip(bump ** 2 * emissive_strength * (0.5 + n), 0, 1)
    return M(col, 0.55 + 0.2 * (1 - bump), 0.0, bump * 0.8 + 0.2 * n, 5, emissive=em)


def kelp_green():
    st = stretched(S, 3, 45, 41)
    rib = 0.5 + 0.5 * np.sin(2 * np.pi * (14 * X / S + 0.3 * st))
    col = ramp(0.6 * st + 0.4 * rib, [(0, "#0b3d22"), (0.5, "#2c9a44"), (1, "#a6e46a")])
    return M(col, 0.6, 0.0, 0.5 * st + 0.5 * rib, 4)


def moss():
    n = fbm(S, 51, 14, 5)
    col = ramp(n, [(0, "#1f4a24"), (0.5, "#3f7a32"), (1, "#8cc152")])
    return M(col, 0.95, 0.0, n, 3)


# ---------------------------------------------------------------- hulls
def hull(base, trim, seed=61, camo=None, trim_every=5, bevel_light=0.06):
    P = 128
    xm, ym = X % P, Y % P
    d = np.minimum(np.minimum(xm, P - 1 - xm), np.minimum(ym, P - 1 - ym))
    seam = (d < 2).astype(float)
    bevel = np.clip(1 - (d - 2) / 7, 0, 1) * (d >= 2)
    n = fbm(S, seed + 1, 7, 3)
    scratch = (stretched(S, 28, 1.1, seed + 2) > 0.9).astype(float) * 0.5 + \
              (stretched(S, 1.1, 22, seed + 3) > 0.92).astype(float) * 0.4
    col = np.ones((S, S, 3)) * rgb01(base)
    if camo:
        a, b, c = [rgb01(k) for k in camo]
        m1 = smoothstep(0.5, 0.56, fbm(S, seed + 7, 40, 3))[..., None]
        m2 = smoothstep(0.55, 0.6, fbm(S, seed + 8, 28, 3))[..., None]
        col = a * (1 - m1) + b * m1
        col = col * (1 - m2) + c * m2
    col = col * (0.93 + 0.12 * n)[..., None] + bevel[..., None] * bevel_light
    col *= (1 - 0.65 * seam)[..., None]
    pi, pj = X // P, Y // P
    has = ((pi + 2 * pj) % trim_every == 0)
    stripe = has & (ym >= 54) & (ym < 74) & (d >= 10)
    col[stripe] = rgb01(trim)
    dxr = np.minimum(abs(xm - 14), abs(xm - (P - 15)))
    dyr = np.minimum(abs(ym - 14), abs(ym - (P - 15)))
    rr = np.hypot(dxr, dyr)
    col += ((rr < 4.2) * 0.14)[..., None]
    col *= (1 - 0.35 * ((rr >= 4.2) & (rr < 6.2)))[..., None]
    col *= (1 - 0.18 * scratch)[..., None]
    rough = 0.38 + 0.25 * scratch + 0.1 * n
    metal = np.where(seam > 0, 0.9, 0.55) - 0.2 * scratch
    height = 0.6 - 0.5 * seam + 0.25 * bevel + 0.2 * (rr < 4.2) - 0.05 * scratch
    return M(col, rough, metal, height, 5)


def carbon_composite():
    w = 0.5 + 0.5 * np.sin(2 * np.pi * X / 16) * np.sin(2 * np.pi * Y / 16)
    tw = 0.5 + 0.5 * np.sin(2 * np.pi * (X + Y) / 32)
    height = 0.6 * w + 0.4 * tw
    col = np.ones((S, S, 3)) * rgb01("#12161e") * (0.7 + 0.8 * height)[..., None]
    return M(col, 0.32 + 0.2 * (1 - height), 0.3, height, 3)


def rusted_metal():
    h = fbm(S, 71, 30, 5)
    rust = smoothstep(0.5, 0.68, fbm(S, 72, 22, 5))
    base = ramp(h, [(0, "#3b4452"), (1, "#6a7587")])
    rc = ramp(fbm(S, 73, 6, 3), [(0, "#7a3515"), (0.5, "#b0561f"), (1, "#d9843a")])
    col = base * (1 - rust[..., None]) + rc * rust[..., None]
    return M(col, 0.55 + 0.4 * rust, 0.8 * (1 - rust), h * 0.5 + rust * 0.5, 5)


def rubber_seal():
    n = noise(S, 0.9, 81)
    col = np.ones((S, S, 3)) * rgb01("#0d1014") * (0.85 + 0.3 * n)[..., None]
    return M(col, 0.95, 0.0, n, 2)


# ---------------------------------------------------------------- crystals
def crystal(lo, mid, hi, seed=91, npts=36):
    f1, f2, ids = worley(S, npts, seed)
    r = rng(seed + 1).random(npts)
    bright = r[ids]
    edge = 1 - smoothstep(0, 4, f2 - f1)
    col = ramp(0.25 + 0.75 * bright, [(0, lo), (0.5, mid), (1, hi)])
    col = col * (1 - 0.5 * edge)[..., None] + edge[..., None] * rgb01(hi) * 0.6
    em = np.clip(0.25 + 0.55 * bright + 0.4 * edge, 0, 1)
    return M(col, 0.12 + 0.1 * (1 - bright), 0.1, bright * 0.5 + (1 - edge) * 0.5, 6, emissive=em)


# ---------------------------------------------------------------- station
def station_floor():
    P = 32
    xm, ym = X % P, Y % P
    hole = ((xm >= 7) & (xm < 25) & (ym >= 7) & (ym < 25)).astype(float)
    rim = ((xm >= 4) & (xm < 28) & (ym >= 4) & (ym < 28)).astype(float) - hole
    n = fbm(S, 101, 12, 3)
    col = np.ones((S, S, 3)) * rgb01("#273445") * (0.85 + 0.3 * n)[..., None]
    col = col * (1 - 0.85 * hole)[..., None] + rim[..., None] * 0.06
    hazard = ((Y // 64) % 8 == 0) & (((X + Y) // 16) % 2 == 0) & ((Y % 64) < 16)
    col[hazard & (hole == 0)] = rgb01("#c98a10") * 0.8
    return M(col, 0.5 + 0.2 * n, 0.75, 0.6 * (1 - hole) + 0.3 * rim, 5)


def station_wall():
    P = 128
    xm, ym = X % P, Y % P
    seam = ((xm < 2) | (ym < 2)).astype(float)
    n = fbm(S, 111, 9, 3)
    col = np.ones((S, S, 3)) * rgb01("#e3ebf5") * (0.94 + 0.1 * n)[..., None]
    band = (Y % 256 >= 90) & (Y % 256 < 150)
    col[band] = rgb01("#1d4f9a") * (0.9 + 0.2 * n[band])[..., None]
    trim = ((Y % 256 >= 84) & (Y % 256 < 90)) | ((Y % 256 >= 150) & (Y % 256 < 156))
    col[trim] = rgb01("#f59e0b")
    line = (Y % 256 >= 117) & (Y % 256 < 123)
    col *= (1 - 0.6 * seam)[..., None]
    em = line.astype(float) * 0.9
    col[line] = rgb01("#7ff0ff")
    return M(col, 0.4 + 0.15 * n, 0.25, 0.7 - 0.5 * seam + 0.1 * band, 4, emissive=em)


def glass_blue():
    n = fbm(S, 121, 70, 3)
    streak = (stretched(S, 60, 2.2, 122) > 0.9).astype(float)
    col = np.ones((S, S, 3)) * rgb01("#8fdcff")
    col = col * (0.9 + 0.1 * n)[..., None] + streak[..., None] * 0.1
    alpha = 0.16 + 0.12 * n + 0.18 * streak
    return M(col, 0.04, 0.0, n * 0.1, 1, alpha=alpha)


def emissive_strip(core, glow):
    v = np.abs(Y - S / 2) / (S / 2)
    core_m = (1 - smoothstep(0.05, 0.18, v))
    glow_m = (1 - smoothstep(0.0, 0.7, v)) ** 2
    base = rgb01("#0b1626")
    col = base * (1 - glow_m[..., None] * 0.3) + rgb01(glow) * (glow_m * 0.45)[..., None]
    col = col * (1 - core_m[..., None]) + rgb01(core) * core_m[..., None]
    seg = (X % 128 < 3).astype(float) * 0.6
    em = np.clip(core_m + 0.4 * glow_m, 0, 1) * (1 - seg)
    return M(col, 0.3, 0.2, 0.5 - 0.2 * core_m, 2, emissive=em)


# ---------------------------------------------------------------- creatures / relics
def bio_skin(base, dot, seed=131):
    f1, f2, ids = worley(S, 260, seed)
    keep = rng(seed + 1).random(260)[ids] > 0.45
    dots = (1 - smoothstep(3, 7, f1)) * keep
    n = fbm(S, seed + 2, 16, 4)
    col = np.ones((S, S, 3)) * rgb01(base) * (0.7 + 0.6 * n)[..., None]
    col = col * (1 - dots[..., None]) + rgb01(dot) * dots[..., None]
    return M(col, 0.5, 0.0, n * 0.4 + dots * 0.4, 3, emissive=np.clip(dots + 0.05 * n, 0, 1))


_SCALE_CACHE = {}


def scale_geometry():
    """Overlapping fish-scale layout (tileable). Returns id, dist-to-center, dy, R."""
    if _SCALE_CACHE:
        return _SCALE_CACHE["g"]
    pitch, R = 32, 20.0
    rows = S // (pitch // 2)
    cid = np.zeros((S, S), dtype=np.int32)
    dist = np.full((S, S), 1e9)
    dyw = np.zeros((S, S))
    k = 0
    for j in range(rows):
        cy = j * (pitch / 2) + pitch / 4
        for i in range(S // pitch):
            cx = (i + 0.5 * (j % 2)) * pitch + pitch / 2
            dx = ((X + 0.5 - cx + S / 2) % S) - S / 2
            dy = ((Y + 0.5 - cy + S / 2) % S) - S / 2
            d = np.hypot(dx, dy)
            m = d < R
            cid[m] = k
            dist[m] = d[m]
            dyw[m] = dy[m]
            k += 1
    _SCALE_CACHE["g"] = (cid, dist, dyw, R, k)
    return _SCALE_CACHE["g"]


def scales(variant):
    cid, d, dyw, R, count = scale_geometry()
    edge = smoothstep(R * 0.78, R, d)
    rim_lit = np.clip(-dyw / R, -1, 1) * 0.5 + 0.5          # lit from above
    shade = (0.55 + 0.55 * (1 - (d / R) ** 2)) * (0.8 + 0.3 * rim_lit)
    n = fbm(S, 141, 18, 4)
    rr = rng(142).random(count)[cid]
    em = None
    if variant == "normal":
        col = ramp(0.55 * n + 0.45 * rr, [(0, "#134fa8"), (0.6, "#2a82ee"), (1, "#f2c230")])
    elif variant == "bioluminescent":
        col = ramp(0.5 * n + 0.2 * rr, [(0, "#04122a"), (1, "#0b3a6e")])
        em = np.clip(edge * 0.9 + 0.08 * n, 0, 1)
    elif variant == "albino":
        col = ramp(0.5 * n + 0.5 * rr, [(0, "#cfd7de"), (1, "#f6f8fa")])
    elif variant == "armored":
        col = ramp(0.5 * n + 0.5 * rr, [(0, "#5a4a30"), (0.6, "#8a7650"), (1, "#b49a62")])
    elif variant == "corrupted":
        col = ramp(0.5 * n + 0.5 * rr, [(0, "#2a0f45"), (1, "#5a2594")])
        em = np.clip(edge * 0.85, 0, 1)
    else:  # rare
        col = ramp((0.6 * (X / S) + 0.4 * n) % 1.0, [(0, "#ff4d6d"), (0.2, "#ffb703"), (0.4, "#4ade80"),
                                                    (0.6, "#00d1ff"), (0.8, "#8b5cf6"), (1.0, "#ff4d6d")])
        em = np.clip(0.2 + 0.25 * shade, 0, 1)
    col = col * shade[..., None]
    if variant == "bioluminescent":
        col = col * (1 - edge[..., None]) + rgb01("#00d1ff") * edge[..., None]
    elif variant == "corrupted":
        col = col * (1 - edge[..., None]) + rgb01("#ff3fd0") * edge[..., None]
    else:
        col = col * (1 - 0.45 * edge[..., None])
    return M(col, 0.35 + 0.3 * (1 - shade), 0.05, shade * 0.8 - edge * 0.3, 5, emissive=em)


def runes_mask(seed=151):
    img = Image.new("L", (S * 2, S * 2), 0)
    dr = ImageDraw.Draw(img)
    P = 128 * 2
    r = rng(seed)
    for cj in range(4):
        for ci in range(4):
            if r.random() < 0.28:
                continue
            ox, oy = ci * P, cj * P
            pts = [(ox + P * (0.22 + 0.28 * a), oy + P * (0.18 + 0.32 * b)) for b in range(3) for a in range(3)]
            for _ in range(int(r.integers(3, 6))):
                a, b = r.integers(0, 9, 2)
                if a != b:
                    dr.line([pts[a], pts[b]], fill=255, width=6)
            c = pts[int(r.integers(0, 9))]
            dr.ellipse([c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7], outline=255, width=5)
    img = img.resize((S, S), Image.LANCZOS)
    return np.asarray(img, dtype=np.float64) / 255


def relic_stone():
    h = fbm(S, 161, 26, 6)
    f1, f2, _ = worley(S, 24, 162)
    block = smoothstep(0, 3, f2 - f1)
    col = ramp(h, [(0, "#3a352e"), (0.5, "#5d564a"), (1, "#8d8272")])
    col *= (0.55 + 0.45 * block)[..., None]
    runes = runes_mask()
    col = col * (1 - 0.6 * runes[..., None])
    glow = runes * (0.7 + 0.3 * noise(S, 4, 163))
    col = col * (1 - glow[..., None]) + rgb01("#7ff0ff") * glow[..., None]
    return M(col, 0.85, 0.05, 0.6 * h + 0.4 * block - 0.3 * runes, 6, emissive=glow)


def relic_obsidian():
    f1, f2, _ = worley(S, 45, 171)
    crack = 1 - smoothstep(0, 2.5, f2 - f1)
    n = fbm(S, 172, 20, 4)
    col = np.ones((S, S, 3)) * rgb01("#090912") * (0.7 + 0.9 * n)[..., None]
    col = col * (1 - crack[..., None]) + rgb01("#a06bff") * crack[..., None]
    return M(col, 0.1 + 0.15 * (1 - crack), 0.2, 0.7 - 0.3 * crack, 6, emissive=crack)


MATERIALS = {
    # name: (builder, category, studs_per_tile, notes)
    "rock_dark": (rock_dark, "terrain", 12, "Shallows/Station rocks, boulders, cliffs"),
    "rock_mossy": (rock_mossy, "terrain", 12, "Kelp Forest rocks and ruins"),
    "sand_seabed": (sand_seabed, "terrain", 16, "Seabed floors in Shallows and Station surroundings"),
    "coral_pink": (lambda: coral(["#ff5d8f", "#ff8a5c", "#ffb3c1", "#ff6f6f"], 0.0, 31), "terrain", 6, "Shallows coral clusters"),
    "coral_purple": (lambda: coral(["#6d3bd6", "#b04bff", "#ff4fd8", "#3b82f6"], 0.9, 33), "terrain", 6, "Twilight Reef coral, emissive glow"),
    "kelp_green": (kelp_green, "terrain", 4, "Kelp blades (vertical streaks)"),
    "moss": (moss, "terrain", 8, "Moss overlay for rocks and ruins"),
    "hull_white": (lambda: hull("#e8eef5", "#f59e0b"), "submarine", 8, "Default sub hull, amber trim"),
    "hull_ocean_blue": (lambda: hull("#1d4f9a", "#e6f1ff", seed=62), "submarine", 8, "Ocean Blue sub variant"),
    "hull_deep_black": (lambda: hull("#161b24", "#00d1ff", seed=63), "submarine", 8, "Deep Black sub variant, aqua trim"),
    "hull_sand": (lambda: hull("#c9b07a", "#7a5a2a", seed=64), "submarine", 8, "Sand (Desert) sub variant"),
    "hull_arctic": (lambda: hull("#dfeaf3", "#3aa6dc", seed=65), "submarine", 8, "Arctic (Ice) sub variant"),
    "hull_camo": (lambda: hull("#4d6b3a", "#2b2f26", seed=66, camo=["#4d6b3a", "#8a8450", "#2c3a27"]), "submarine", 8, "Camo (Stealth) sub variant"),
    "carbon_composite": (carbon_composite, "submarine", 4, "Hull detailing, carbon fibre"),
    "rusted_metal": (rusted_metal, "terrain", 8, "Wrecks, debris, old structures"),
    "rubber_seal": (rubber_seal, "submarine", 4, "Seals and gaskets"),
    "crystal_blue": (lambda: crystal("#0b3d91", "#1fa2ff", "#aef2ff", 91), "resource", 6, "Crystal / Rare Crystal nodes"),
    "crystal_purple": (lambda: crystal("#3b1a8a", "#7a3cff", "#e0b8ff", 92), "resource", 6, "Twilight Reef crystals"),
    "crystal_ruby": (lambda: crystal("#7a0d2e", "#ff3b6b", "#ffc0d0", 93), "resource", 6, "Ruby Crystal nodes"),
    "station_floor": (station_floor, "station", 8, "Grated deck floor with hazard marks"),
    "station_wall": (station_wall, "station", 10, "Interior wall: white panels, blue band, aqua light line"),
    "glass_blue": (glass_blue, "station", 8, "Windows, domes; color map has alpha"),
    "emissive_strip_aqua": (lambda: emissive_strip("#d6faff", "#00d1ff"), "station", 8, "Light strips (aqua)"),
    "emissive_strip_amber": (lambda: emissive_strip("#fff0c2", "#f59e0b"), "station", 8, "Light strips (amber)"),
    "emissive_strip_red": (lambda: emissive_strip("#ffd2d2", "#ef4444"), "station", 8, "Warning strips (crimson)"),
    "bio_skin_aqua": (lambda: bio_skin("#06142c", "#38e1ff", 131), "creature", 6, "Bioluminescent dots (aqua)"),
    "bio_skin_purple": (lambda: bio_skin("#14082c", "#c084ff", 132), "creature", 6, "Bioluminescent dots (purple)"),
    "bio_skin_teal": (lambda: bio_skin("#06201c", "#2dd4bf", 133), "creature", 6, "Bioluminescent dots (teal)"),
    "scales_normal": (lambda: scales("normal"), "creature", 4, "Creature scales: Normal"),
    "scales_bioluminescent": (lambda: scales("bioluminescent"), "creature", 4, "Creature scales: Bioluminescent"),
    "scales_albino": (lambda: scales("albino"), "creature", 4, "Creature scales: Albino"),
    "scales_armored": (lambda: scales("armored"), "creature", 4, "Creature scales: Armored"),
    "scales_corrupted": (lambda: scales("corrupted"), "creature", 4, "Creature scales: Corrupted"),
    "scales_rare": (lambda: scales("rare"), "creature", 4, "Creature scales: Rare (rainbow)"),
    "relic_stone": (relic_stone, "relic", 6, "Ancient stone with glowing runes"),
    "relic_obsidian": (relic_obsidian, "relic", 6, "Obsidian Core with violet fractures"),
}



# ================================================================= v2 upgrades
def lit(col, height, k=1.0, light=(-0.6, -0.8)):
    """Bake soft key-light + ambient occlusion into a colour map so rocks read as 3D at a glance."""
    gx = (np.roll(height, -1, 1) - np.roll(height, 1, 1)) * 0.5
    gy = (np.roll(height, -1, 0) - np.roll(height, 1, 0)) * 0.5
    sh = np.clip(-(gx * light[0] + gy * light[1]) * 14 * k, -1, 1)
    ao = height - gaussian_filter(height, 10, mode="wrap")
    ao = np.clip(ao * 3.0, -0.6, 0.4)
    return np.clip(col * (1 + 0.38 * sh + 0.5 * ao)[..., None], 0, 1)


def rock_dark_v2():
    f1, f2, ids = worley(S, 34, 3)
    bevel = smoothstep(0, 16, f2 - f1)                     # soft rounded faces, not thin lines
    face = rng(4).random(34)[ids]
    form = fbm(S, 5, 56, 5)
    detail = fbm(S, 6, 9, 4)
    ridge = ridged(fbm(S, 7, 24, 4))
    height = 0.55 * bevel + 0.25 * form + 0.12 * ridge + 0.08 * detail
    base = ramp(0.35 * face + 0.35 * form + 0.3 * detail, [(0, "#0c1424"), (0.5, "#27384f"), (1, "#566a86")])
    crack_mask = smoothstep(0.55, 0.7, fbm(S, 8, 36, 3))
    crack = (1 - smoothstep(0, 2.2, f2 - f1)) * crack_mask
    col = lit(base, height, 1.2) * (1 - 0.8 * crack)[..., None]
    speck = (noise(S, 0.7, 9) > 0.93) * 0.12
    col = np.clip(col + speck[..., None] * 0.5, 0, 1)
    return M(col, 0.82 + 0.12 * detail, 0.0, height - 0.5 * crack, 7)


def rock_mossy_v2():
    b = rock_dark_v2()
    moss_mask = smoothstep(0.5, 0.68, fbm(S, 11, 32, 5)) * smoothstep(0.25, 0.55, b["height"])
    mc = lit(ramp(fbm(S, 12, 5, 3), [(0, "#1c3f1c"), (0.5, "#3c7a30"), (1, "#8fc653")]), b["height"] + moss_mask * 0.25, 0.8)
    col = b["color"] * (1 - moss_mask[..., None]) + mc * moss_mask[..., None]
    return M(col, 0.9, 0.0, b["height"] + moss_mask * 0.2, 6)


def cliff_layered():
    warp = fbm(S, 21, 70, 3)
    strata = 0.5 + 0.5 * np.sin(2 * np.pi * (7 * Y / S + 0.55 * (warp - 0.5)))
    thin = 0.5 + 0.5 * np.sin(2 * np.pi * (29 * Y / S + 1.4 * (warp - 0.5)))
    vert = stretched(S, 1.2, 40, 22)
    erosion = ridged(fbm(S, 23, 28, 4))
    height = 0.45 * strata + 0.15 * thin + 0.2 * vert + 0.2 * erosion
    tone = ramp(0.5 * strata + 0.3 * erosion + 0.2 * thin, [(0, "#101a2c"), (0.5, "#34455e"), (1, "#6c809a")])
    tint = ramp(warp, [(0, "#2a2f45"), (1, "#3a4a5a")])
    col = lit(tone * 0.8 + tint * 0.2, height, 1.2)
    return M(col, 0.86, 0.0, height, 8)


def pebbles_seabed():
    f1, f2, ids = worley(S, 180, 31)
    ratio = f1 / (f1 + f2 + 1e-9)                          # 0 at pebble centre, 0.5 on the cell border
    rad = 0.40 + 0.08 * rng(32).random(180)[ids]
    dome = np.clip(1 - (ratio / rad) ** 2, 0, 1) ** 0.55
    pc = np.array([rgb01(c) for c in ["#8a7d63", "#b3a47c", "#6f7a86", "#a29a8c", "#54606e", "#c9b98e"]])
    base = pc[ids % len(pc)] * (0.82 + 0.34 * rng(33).random(180)[ids])[..., None]
    gap = np.ones((S, S, 3)) * rgb01("#2e281c")
    m = smoothstep(0, 0.18, dome)[..., None]
    col = lit(base * m + gap * (1 - m), dome * 0.9, 1.5)
    col *= (0.92 + 0.16 * fbm(S, 34, 10, 3))[..., None]
    return M(col, 0.78, 0.0, dome, 7)


def ruins_blocks():
    bw, bh = 128, 64
    row = Y // bh
    off = (row % 2) * (bw // 2)
    xm, ym = (X + off) % bw, Y % bh
    d = np.minimum(np.minimum(xm, bw - 1 - xm), np.minimum(ym, bh - 1 - ym))
    bid = (((X + off) // bw) + row * 7).astype(int)
    shade = rng(41).random(64)[bid % 64]
    bevel = smoothstep(0, 9, d)
    joint = 1 - smoothstep(0, 3, d)
    wear = fbm(S, 42, 16, 5)
    height = 0.7 * bevel + 0.2 * wear + 0.1 * noise(S, 1.0, 43)
    base = ramp(0.45 * shade + 0.55 * wear, [(0, "#2a3a3c"), (0.5, "#4f6462"), (1, "#7f9690")])
    moss_m = smoothstep(0.55, 0.72, fbm(S, 44, 20, 4)) * (0.4 + 0.6 * joint)
    mc = ramp(fbm(S, 45, 5, 3), [(0, "#1d4a26"), (1, "#6eb34a")])
    col = base * (1 - moss_m[..., None]) + mc * moss_m[..., None]
    col = lit(col, height, 1.3) * (1 - 0.7 * joint)[..., None]
    return M(col, 0.88, 0.0, height - moss_m * 0.1, 7)


MATERIALS["rock_dark"] = (rock_dark_v2, "terrain", 12, "Shallows/Station rocks, boulders, cliffs (soft faceted, baked AO)")
MATERIALS["rock_mossy"] = (rock_mossy_v2, "terrain", 12, "Kelp Forest rocks and ruins (moss in crevices)")
MATERIALS["cliff_layered"] = (cliff_layered, "terrain", 16, "Layered cliff strata for canyon walls and zone borders")
MATERIALS["pebbles_seabed"] = (pebbles_seabed, "terrain", 10, "Pebble seabed for Kelp Forest / Station surroundings")
MATERIALS["ruins_blocks"] = (ruins_blocks, "terrain", 10, "Ancient masonry for Kelp ruins and Lost Ruins teaser")


def build_all():
    report = {}
    for name, (fn, cat, studs, note) in MATERIALS.items():
        m = fn()
        d = os.path.join(OUT, name)
        col = np.clip(m["color"], 0, 1)
        if m["alpha"] is not None:
            col = np.dstack([col, np.clip(m["alpha"], 0, 1)])
        save(os.path.join(d, "color.png"), col)
        save(os.path.join(d, "normal.png"), normal_from_height(m["height"], m["nstr"]))
        save(os.path.join(d, "roughness.png"), np.clip(m["rough"], 0, 1))
        save(os.path.join(d, "metalness.png"), np.clip(m["metal"], 0, 1))
        maps = ["color", "normal", "roughness", "metalness"]
        if m["emissive"] is not None:
            save(os.path.join(d, "emissive.png"), np.clip(m["emissive"], 0, 1))
            maps.append("emissive")
        report[name] = dict(category=cat, studs_per_tile=studs, notes=note, maps=maps,
                            has_alpha=m["alpha"] is not None,
                            seam_ratio=round(seam_error(np.clip(m["color"], 0, 1)), 2))
        print(f"{name:24s} seam={report[name]['seam_ratio']}", flush=True)
    with open(os.path.join(OUT, "_report.json"), "w") as f:
        json.dump(report, f, indent=1)
    return report


if __name__ == "__main__":
    build_all()
