"""Generate VFX / HUD overlay textures: particles, beams, sonar, caustics, vignettes."""
import json
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
from tex_common import *  # noqa

OUT = os.path.join(ROOT, "vfx")
REPORT = {}
SS = 4


def rgba_arr(rgb, alpha):
    h, w = alpha.shape
    out = np.zeros((h, w, 4))
    out[..., :3] = rgb01(rgb) if isinstance(rgb, str) else rgb
    out[..., 3] = np.clip(alpha, 0, 1)
    return out


def put(rel, arr_or_img, **meta):
    path = os.path.join(OUT, rel)
    if isinstance(arr_or_img, Image.Image):
        save_img(path, arr_or_img)
        size = list(arr_or_img.size)
    else:
        save(path, arr_or_img)
        size = [arr_or_img.shape[1], arr_or_img.shape[0]]
    REPORT[rel] = dict(size=size, **meta)


def radial(S, power=2.0, hard=0.0):
    y, x = np.mgrid[0:S, 0:S]
    r = np.hypot(x - S / 2 + 0.5, y - S / 2 + 0.5) / (S / 2)
    return np.clip(1 - r, 0, 1) ** power, r


# ------------------------------------------------------------ particles
def particles():
    a, _ = radial(64, 2.2)
    put("particles/particle_marine_snow.png", rgba_arr("#d6ecff", a * 0.9), usage="ParticleEmitter.Texture for marine snow (camera-relative, tiny, low rate).")
    a, r = radial(128, 2.0)
    put("particles/particle_glow.png", rgba_arr("#ffffff", a), usage="Soft additive glow. Tint with Color. Bioluminescence, lantern flare.")
    S = 64
    y, x = np.mgrid[0:S, 0:S]
    r = np.hypot(x - S / 2 + .5, y - S / 2 + .5) / (S / 2)
    ring = np.exp(-((r - 0.78) / 0.12) ** 2)
    hl = np.exp(-(((x - S * 0.35) ** 2 + (y - S * 0.32) ** 2) / (S * 0.07) ** 2))
    fill = np.clip(1 - r, 0, 1) * 0.12
    put("particles/particle_bubble.png", rgba_arr("#e8f8ff", np.clip(ring * 0.85 + hl * 0.9 + fill, 0, 1)), usage="Single bubble.")
    # 4x4 atlas of bubbles with varied highlight/size (Flipbook Grid4x4)
    atlas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    rr = rng(5)
    for i in range(16):
        S2 = 64
        sc = 0.55 + 0.4 * rr.random()
        y2, x2 = np.mgrid[0:S2, 0:S2]
        r2 = np.hypot(x2 - S2 / 2 + .5, y2 - S2 / 2 + .5) / (S2 / 2 * sc)
        ring2 = np.exp(-((r2 - 0.85) / 0.16) ** 2) * (r2 < 1.4)
        h2 = np.exp(-(((x2 - S2 * (0.5 - 0.15 * sc)) ** 2 + (y2 - S2 * (0.5 - 0.17 * sc)) ** 2) / (S2 * 0.06) ** 2))
        al = np.clip(ring2 * 0.85 + h2 * 0.9 + np.clip(1 - r2, 0, 1) * 0.1, 0, 1)
        tile = to_img(rgba_arr("#e8f8ff", al))
        atlas.paste(tile, ((i % 4) * 64, (i // 4) * 64))
    put("particles/particle_bubble_atlas.png", atlas, usage="ParticleEmitter flipbook (FlipbookLayout=Grid4x4, mode Random) for vents/propulsion.")
    # sparkle (4-point)
    S = 64
    y, x = np.mgrid[0:S, 0:S]
    dx, dy = np.abs(x - S / 2 + .5) / (S / 2), np.abs(y - S / 2 + .5) / (S / 2)
    spark = np.exp(-(dx * 14)) * np.exp(-(dy * 1.3) ** 2) + np.exp(-(dy * 14)) * np.exp(-(dx * 1.3) ** 2)
    core = np.exp(-((dx ** 2 + dy ** 2) * 18))
    put("particles/particle_spark.png", rgba_arr("#ffffff", np.clip(spark * 0.9 + core, 0, 1)), usage="Hull impact sparks / discovery sparkle.")
    # soft ring
    S = 128
    y, x = np.mgrid[0:S, 0:S]
    r = np.hypot(x - S / 2 + .5, y - S / 2 + .5) / (S / 2)
    put("particles/particle_ring.png", rgba_arr("#ffffff", np.exp(-((r - 0.8) / 0.09) ** 2)), usage="Expanding pulse ring (scan complete, pings).")
    # thermal flare
    a, r = radial(128, 1.6)
    col = ramp(np.clip(1 - r, 0, 1), [(0, "#ff5a1f"), (0.5, "#ffb020"), (1, "#fff3c0")])
    put("particles/particle_thermal_flare.png", np.dstack([col, a]), usage="Thermal vent flare / Anomalous Shift.")
    # electric arc
    img = Image.new("RGBA", (256 * SS // SS * SS, 64 * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rr = rng(9)
    pts = [(0, 32 * SS)]
    for i in range(1, 12):
        pts.append((i * 256 * SS / 11, (32 + rr.integers(-14, 15)) * SS))
    for w, c in ((14, (0, 209, 255, 70)), (8, (110, 235, 255, 140)), (3, (255, 255, 255, 255))):
        d.line(pts, fill=c, width=w * SS // 2, joint="curve")
    img = img.filter(ImageFilter.GaussianBlur(1.0 * SS)).resize((256, 64), Image.LANCZOS)
    put("particles/particle_electric_arc.png", img, usage="Hazard interaction: lightweight electric arc (Beam texture).")


# ------------------------------------------------------------ beams & overlays
def beams():
    # lantern streaks (tileable both ways)
    S = 256
    st = stretched(S, 5, 70, 301)
    a = smoothstep(0.35, 0.95, st) * 0.55
    put("beams/lantern_beam_streaks.png", rgba_arr("#fff1c2", a), tileable=True, usage="Scrolling translucent texture on the lantern cone mesh/beam (animate Offset).")
    # beam falloff gradient (1D along length)
    W, H = 256, 64
    x = np.linspace(0, 1, W)[None, :]
    y = np.abs(np.linspace(-1, 1, H))[:, None]
    a = (1 - y ** 2) ** 2 * (1 - x) ** 1.4
    put("beams/beam_falloff.png", rgba_arr("#fff7d6", a), usage="Beam.Texture: bright at origin, fades along length and sideways.")
    # scanner sheet
    S = 256
    y, x = np.mgrid[0:S, 0:S]
    lines = 0.5 + 0.5 * np.sin(2 * np.pi * y / 16)
    edge = 1 - smoothstep(0.55, 1.0, np.abs(x / S * 2 - 1))
    a = (0.12 + 0.35 * smoothstep(0.55, 1.0, lines)) * edge
    put("beams/scanner_sheet.png", rgba_arr("#6beaff", a), usage="Thin translucent forward light sheet for the scanner beam.")
    # light rays (tileable)
    S = 512
    st = stretched(S, 16, 160, 311)
    a = smoothstep(0.55, 0.92, st) * 0.5
    put("beams/light_rays_tile.png", rgba_arr("#bfe9ff", a), tileable=True, usage="God-rays overlay in Shallows/Kelp (fade top-to-bottom with UIGradient or Transparency).")
    # caustics (tileable)
    S = 512
    tot = np.zeros((S, S))
    for i, (n, sd) in enumerate(((34, 321), (60, 322))):
        f1, f2, _ = worley(S, n, sd)
        tot += (1 - smoothstep(0, 3.2 + i, f2 - f1)) * (0.8 - 0.25 * i)
    wob = fbm(S, 323, 40, 3)
    a = np.clip(tot, 0, 1) * (0.6 + 0.5 * wob)
    put("beams/caustics_tile.png", rgba_arr("#c8f6ff", a * 0.9), tileable=True, usage="Light caustics: project on seabed as Decal/Texture on Shallows (additive, animate).")
    # marine snow overlay tile
    S = 512
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rr = rng(331)
    for _ in range(260):
        x, y = rr.random() * S, rr.random() * S
        r = 0.8 + rr.random() * 1.8
        al = int(70 + rr.random() * 150)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=(214, 236, 255, al))
    put("beams/marine_snow_tile.png", img.filter(ImageFilter.GaussianBlur(0.6)), tileable=True, usage="Screen-space marine snow (ImageLabel tile, scroll slowly). Prefer ParticleEmitter in 3D.")


def vignettes():
    S = 512
    y, x = np.mgrid[0:S, 0:S]
    r = np.hypot(x - S / 2 + .5, y - S / 2 + .5) / (S / 2 * 1.2)
    a = smoothstep(0.45, 1.05, r)
    put("hud/vignette_navy.png", rgba_arr("#020a1c", a * 0.85), usage="Depth transition screen-edge tint (fullscreen, ZIndex under HUD).")
    put("hud/vignette_alert.png", rgba_arr("#b3121f", a * 0.7), usage="Critical Hull/Battery warning edge (no white flash, no strobe; fade slowly <=1Hz).")
    put("hud/vignette_amber.png", rgba_arr("#d98a00", a * 0.5), usage="Low reserve warning edge tint.")


# ------------------------------------------------------------ HUD sonar/scanner
def hud_art():
    S = 512
    img = Image.new("RGBA", (S * SS // SS, S), (0, 0, 0, 0))
    big = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    c = S
    teal = (20, 184, 166)
    for i, r in enumerate((0.25, 0.5, 0.75, 1.0)):
        rad = r * (S - 6)
        d.ellipse([c - rad, c - rad, c + rad, c + rad], outline=teal + ((200 if r == 1.0 else 110),), width=3 if r == 1.0 else 2)
    d.line([(c, 6), (c, 2 * S - 6)], fill=teal + (90,), width=2)
    d.line([(6, c), (2 * S - 6, c)], fill=teal + (90,), width=2)
    for k in range(72):
        a = math.radians(k * 5)
        ln = 22 if k % 6 == 0 else 10
        r0 = S - 6
        d.line([(c + r0 * math.cos(a), c + r0 * math.sin(a)), (c + (r0 - ln) * math.cos(a), c + (r0 - ln) * math.sin(a))], fill=teal + (200 if k % 6 == 0 else 120,), width=3)
    put("hud/sonar_radar_bg.png", big.resize((S, S), Image.LANCZOS), usage="Sonar HUD background (circular). Square ImageLabel + UIAspectRatioConstraint.")
    # sweep wedge
    arr = np.zeros((S, S, 4))
    y, x = np.mgrid[0:S, 0:S]
    ang = (np.degrees(np.arctan2(y - S / 2 + .5, x - S / 2 + .5)) + 360) % 360
    rr = np.hypot(x - S / 2 + .5, y - S / 2 + .5) / (S / 2)
    a = np.clip(1 - ang / 80.0, 0, 1) ** 1.6 * (rr < 1) * (0.55 * (0.4 + 0.6 * rr))
    put("hud/sonar_sweep.png", rgba_arr("#2ad8ff", a), usage="Rotate this ImageLabel (Rotation) for the sonar sweep; event-driven pings preferred (no per-frame polling).")
    # sonar ring (3D expanding ring mesh/ui)
    S2 = 512
    y, x = np.mgrid[0:S2, 0:S2]
    rr2 = np.hypot(x - S2 / 2 + .5, y - S2 / 2 + .5) / (S2 / 2)
    a = np.exp(-((rr2 - 0.9) / 0.05) ** 2) + 0.25 * np.exp(-((rr2 - 0.8) / 0.12) ** 2)
    put("hud/sonar_ring.png", rgba_arr("#6beaff", np.clip(a, 0, 1)), usage="Expanding sonar pulse (UI scale tween or ring mesh texture).")
    # scan reticle
    big = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    cy = 256
    cyan = (42, 216, 255)
    L, T = 70, 6
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0, y0 = cy + sx * 210, cy + sy * 210
            d.line([(x0, y0), (x0 - sx * L, y0)], fill=cyan + (255,), width=T)
            d.line([(x0, y0), (x0, y0 - sy * L)], fill=cyan + (255,), width=T)
    d.ellipse([cy - 90, cy - 90, cy + 90, cy + 90], outline=cyan + (160,), width=4)
    d.ellipse([cy - 6, cy - 6, cy + 6, cy + 6], fill=cyan + (255,))
    for a_ in range(0, 360, 90):
        r = math.radians(a_)
        d.line([(cy + 100 * math.cos(r), cy + 100 * math.sin(r)), (cy + 130 * math.cos(r), cy + 130 * math.sin(r))], fill=cyan + (220,), width=4)
    put("hud/scan_reticle.png", big.resize((256, 256), Image.LANCZOS), usage="Scanner lock reticle (BillboardGui on target).")
    # holographic target ring
    big = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    for k in range(24):
        d.arc([30, 30, 482, 482], k * 15, k * 15 + 9, fill=(42, 216, 255, 255), width=8)
    d.ellipse([60, 60, 452, 452], outline=(42, 216, 255, 90), width=4)
    put("hud/target_ring_holo.png", big.resize((256, 256), Image.LANCZOS), usage="Species Scanned: clean holographic ring + brief cyan highlight.")
    # recall ring (segmented light ring)
    big = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    for k in range(8):
        d.arc([20, 20, 492, 492], k * 45 + 3, k * 45 + 36, fill=(190, 245, 255, 255), width=18)
    glow = big.filter(ImageFilter.GaussianBlur(10))
    big = Image.alpha_composite(glow, big)
    put("hud/recall_ring.png", big, usage="Emergency Recall light-ring presentation (rotate + scale; with cavitation bubbles).")
    # bio pulse ring (soft, purple/teal tintable)
    S3 = 256
    y, x = np.mgrid[0:S3, 0:S3]
    r3 = np.hypot(x - S3 / 2 + .5, y - S3 / 2 + .5) / (S3 / 2)
    a = np.exp(-((r3 - 0.7) / 0.22) ** 2) * 0.9
    put("hud/bio_pulse.png", rgba_arr("#ffffff", a), usage="Bioluminescent pulse (tint per creature). Animate ImageTransparency, not per-frame logic.")


def depth_gradients():
    # per-zone vertical background gradients (UI backdrops for station terminals, loading, codex)
    zones = {
        "shallows": ["#0e7fb8", "#0a4f86", "#073663"],
        "kelp_forest": ["#0b6e5a", "#0a4a46", "#08303a"],
        "twilight_reef": ["#3a1c78", "#1d1052", "#0b0a2b"],
        "station": ["#0b4a8a", "#082e5c", "#061a3a"],
        "abyss": ["#07162f", "#040c1d", "#020610"],
    }
    for z, cols in zones.items():
        t = np.linspace(0, 1, 256)
        col = ramp(t, [(0, cols[0]), (0.55, cols[1]), (1, cols[2])])
        arr = np.repeat(col[:, None, :], 16, axis=1)
        put(f"backdrops/depth_{z}.png", arr, usage="Vertical zone gradient (ImageLabel Stretch) for terminals / loading / codex backgrounds.")


def build_all():
    particles()
    beams()
    vignettes()
    hud_art()
    depth_gradients()
    with open(os.path.join(OUT, "_report.json"), "w") as f:
        json.dump(REPORT, f, indent=1)
    print(len(REPORT), "vfx textures")


if __name__ == "__main__":
    build_all()
