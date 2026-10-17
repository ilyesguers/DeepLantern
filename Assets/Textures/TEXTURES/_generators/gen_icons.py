"""Generate Deep Lantern icon set: plated colour icons (128px) + tintable white glyphs."""
import json
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np
from scipy.ndimage import gaussian_filter, minimum_filter

sys.path.insert(0, os.path.dirname(__file__))
from tex_common import *  # noqa

SS = 4
N = 128
OUT = os.path.join(ROOT, "icons")
PAL.update({"navy2": "#12315c", "lgray": "#cbd5e1", "dgray": "#475569", "cyan2": "#7ff0ff"})


def col(name, a=255):
    r, g, b = hex2rgb(PAL.get(name, name))
    return (r, g, b, a)


# ----------------------------------------------------------- op helpers
def hexp(cx, cy, r, rot=30):
    return [(cx + r * math.cos(math.radians(rot + 60 * i)), cy + r * math.sin(math.radians(rot + 60 * i))) for i in range(6)]


def star(cx, cy, ro, ri, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.radians(rot + 180 / n * i)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def gear(cx, cy, ro, ri, teeth):
    pts = []
    for i in range(teeth):
        a0 = 360 / teeth * i
        for da, r in ((-0.22, ri), (-0.12, ro), (0.12, ro), (0.22, ri)):
            a = math.radians(a0 + da * 360 / teeth)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def gem(main, light, dark):
    return [("p", [(50, 10), (82, 34), (70, 86), (30, 86), (18, 34)], main),
            ("p", [(50, 10), (82, 34), (50, 42), (18, 34)], light),
            ("p", [(50, 42), (82, 34), (70, 86)], dark),
            ("p", [(50, 42), (18, 34), (30, 86)], main),
            ("l", [(50, 42), (50, 86)], light, 2)]


def lantern(body="amber", cap="gold", flame="white", glass_a=None):
    return [("a", (34, 6, 66, 38), 195, 345, "lgray", 4),
            ("p", [(36, 24), (64, 24), (70, 34), (30, 34)], cap),
            ("r", (30, 34, 70, 74), 7, body),
            ("e", (40, 42, 60, 66), flame),
            ("r", (32, 72, 68, 84), 4, cap),
            ("l", [(30, 50), (70, 50)], "dark", 2)]


def sub(body="aqua", trim="white", fin="navy2", extra=None):
    ops = [("p", [(10, 52), (2, 38), (2, 66)], fin),
           ("e", (8, 38, 92, 68), body),
           ("r", (40, 26, 62, 44), 5, trim),
           ("l", [(51, 26), (51, 14), (60, 14)], "lgray", 3),
           ("e", (62, 46, 78, 60), "dark"), ("e", (66, 49, 74, 57), "cyan2"),
           ("p", [(86, 53), (98, 46), (98, 60)], "amber")]
    return ops + (extra or [])


def fish(body, fin, eye="white", extra=None):
    ops = [("p", [(22, 50), (4, 32), (4, 68)], fin),
           ("e", (16, 28, 84, 72), body),
           ("p", [(42, 30), (58, 14), (66, 32)], fin),
           ("e", (66, 40, 76, 50), eye), ("e", (70, 43, 75, 48), "dark")]
    return ops + (extra or [])


def dome(base="aqua", glass="cyan2", n=1, locked=False):
    ops = [("r", (6, 74, 94, 88), 4, "gray")]
    for i in range(n):
        cx = 50 + (i - (n - 1) / 2) * 30 if n > 1 else 50
        r = 22 if n > 1 else 32
        ops += [("e", (cx - r, 74 - r * 1.5, cx + r, 78), base), ("e", (cx - r + 6, 74 - r * 1.5 + 6, cx + r - 6, 76), glass)]
    ops += [("l", [(50, 24 if n == 1 else 30), (50, 8)], "lgray", 3), ("e", (45, 3, 55, 13), "amber")]
    return ops


# ------------------------------------------------------------ icon sets
HUD = {
    "battery_oxygen": ("aqua", [("r", (16, 28, 78, 72), 7, "aqua"), ("r", (78, 40, 88, 60), 3, "aqua"),
                                ("p", [(52, 33), (38, 54), (48, 54), (43, 68), (62, 46), (51, 46)], "dark")]),
    "hull": ("blue", [("p", [(50, 10), (84, 24), (84, 54), (50, 90), (16, 54), (16, 24)], "blue"),
                      ("p", [(50, 22), (72, 31), (72, 51), (50, 77), (28, 51), (28, 31)], "navy2"),
                      ("l", [(38, 46), (48, 58), (64, 36)], "white", 6)]),
    "cargo": ("amber", [("l", [(32, 30), (32, 18), (68, 18), (68, 30)], "gold", 5),
                        ("r", (14, 30, 86, 82), 6, "amber"), ("l", [(14, 52), (86, 52)], "dark", 5),
                        ("r", (40, 46, 60, 60), 3, "dark")]),
    "depth": ("aqua", [("p", [(50, 90), (24, 60), (42, 60), (42, 12), (58, 12), (58, 60), (76, 60)], "aqua"),
                       ("l", [(8, 36), (18, 30), (28, 36)], "teal", 4), ("l", [(72, 36), (82, 30), (92, 36)], "teal", 4)]),
    "scanner": ("aqua", [("ring", (16, 16, 84, 84), "aqua", 6), ("ring", (32, 32, 68, 68), "aqua", 5), ("e", (44, 44, 56, 56), "white"),
                         ("l", [(50, 4), (50, 20)], "aqua", 5), ("l", [(50, 80), (50, 96)], "aqua", 5),
                         ("l", [(4, 50), (20, 50)], "aqua", 5), ("l", [(80, 50), (96, 50)], "aqua", 5)]),
    "sonar": ("aqua", [("e", (44, 44, 56, 56), "aqua"), ("a", (30, 30, 70, 70), -50, 50, "aqua", 6), ("a", (16, 16, 84, 84), -50, 50, "aqua", 6),
                       ("a", (2, 2, 98, 98), -50, 50, "aqua", 6), ("a", (30, 30, 70, 70), 130, 230, "aqua", 6), ("a", (16, 16, 84, 84), 130, 230, "aqua", 6)]),
    "lantern": ("amber", lantern()),
    "recall": ("aqua", [("a", (18, 18, 82, 82), 35, 325, "aqua", 9), ("p", [(66, 22), (90, 28), (76, 50)], "aqua"), ("e", (42, 42, 58, 58), "white")]),
    "ping": ("aqua", [("e", (28, 12, 72, 56), "aqua"), ("p", [(33, 46), (67, 46), (50, 90)], "aqua"), ("e", (42, 25, 58, 41), "dark")]),
    "objective": ("aqua", [("ring", (12, 12, 88, 88), "aqua", 6), ("p", [(50, 26), (74, 50), (50, 74), (26, 50)], "aqua"), ("e", (43, 43, 57, 57), "dark")]),
    "research_data": ("blue", [("r", (36, 20, 64, 88), 10, "blue"), ("r", (30, 10, 70, 26), 5, "lgray"), ("r", (40, 44, 60, 80), 7, "aqua"),
                               ("l", [(44, 36), (56, 36)], "white", 3)]),
    "credits": ("gold", [("p", hexp(50, 50, 44), "gold"), ("p", hexp(50, 50, 33), "amber"),
                         ("p", [(50, 30), (66, 40), (66, 60), (50, 70), (34, 60), (34, 40)], "gold"), ("l", [(50, 30), (50, 70)], "amber", 3)]),
    "warning": ("amber", [("p", [(50, 8), (94, 86), (6, 86)], "amber"), ("l", [(50, 36), (50, 60)], "dark", 9), ("e", (44, 66, 56, 78), "dark")]),
    "hazard": ("red", [("p", [(50, 8), (94, 86), (6, 86)], "red"), ("p", [(54, 30), (40, 58), (50, 58), (46, 76), (62, 48), (52, 48)], "dark")]),
    "check": ("green", [("l", [(18, 54), (42, 78), (84, 26)], "green", 13)]),
    "close": ("red", [("l", [(22, 22), (78, 78)], "red", 13), ("l", [(78, 22), (22, 78)], "red", 13)]),
    "settings": ("gray", [("p", gear(50, 50, 44, 34, 8), "lgray"), ("e", (36, 36, 64, 64), "dark")]),
    "codex": ("aqua", [("p", [(50, 24), (10, 16), (10, 78), (50, 86)], "aqua"), ("p", [(50, 24), (90, 16), (90, 78), (50, 86)], "blue"),
                       ("l", [(50, 24), (50, 86)], "white", 3), ("l", [(20, 36), (40, 40)], "white", 3), ("l", [(80, 36), (60, 40)], "white", 3)]),
    "quest": ("teal", [("r", (22, 14, 78, 90), 6, "teal"), ("r", (36, 6, 64, 22), 5, "lgray"), ("l", [(34, 40), (66, 40)], "white", 5),
                       ("l", [(34, 54), (66, 54)], "white", 5), ("l", [(34, 68), (54, 68)], "white", 5)]),
    "station": ("aqua", dome()),
    "lock": ("gray", [("a", (30, 8, 70, 56), 180, 360, "lgray", 9), ("r", (20, 44, 80, 90), 7, "lgray"), ("e", (43, 58, 57, 72), "dark"), ("r", (47, 68, 53, 80), 2, "dark")]),
    "secure_cargo_buoy": ("amber", [("e", (20, 36, 80, 94), "amber"), ("l", [(20, 66), (80, 66)], "white", 6),
                                    ("l", [(50, 36), (50, 12)], "lgray", 4), ("e", (43, 4, 57, 18), "red")]),
}

ROLES = {
    "role_pilot": ("aqua", [("ring", (14, 14, 86, 86), "aqua", 8), ("e", (40, 40, 60, 60), "aqua"), ("l", [(50, 14), (50, 40)], "aqua", 7),
                            ("l", [(18, 66), (40, 54)], "aqua", 7), ("l", [(82, 66), (60, 54)], "aqua", 7)]),
    "role_lamp_operator": ("amber", [("p", [(54, 38), (98, 18), (98, 82), (54, 62)], "gold"), ("r", (8, 32, 58, 68), 9, "amber"), ("e", (46, 38, 64, 62), "white")]),
    "role_navigator": ("teal", [("ring", (12, 12, 88, 88), "teal", 7), ("p", [(50, 20), (60, 50), (50, 80), (40, 50)], "dgray"),
                                ("p", [(50, 20), (60, 50), (40, 50)], "red"), ("e", (45, 45, 55, 55), "white")]),
    "role_collector": ("green", [("l", [(16, 88), (36, 56), (60, 56)], "green", 10), ("l", [(60, 56), (82, 34)], "green", 10), ("l", [(60, 56), (82, 78)], "green", 10),
                                 ("e", (8, 80, 24, 96), "lgray")]),
    "ping_scan_target": ("aqua", HUD["scanner"][1]),
    "ping_hazard_ahead": ("red", HUD["hazard"][1]),
    "ping_cargo_detected": ("amber", HUD["cargo"][1]),
    "ping_return_to_dock": ("aqua", [("p", [(8, 50), (44, 18), (44, 38), (92, 38), (92, 62), (44, 62), (44, 82)], "aqua")]),
    "ping_check_battery": ("amber", HUD["battery_oxygen"][1]),
}

RESOURCES = {
    "crystal": ("blue", gem("blue", "cyan2", "navy2")),
    "rare_crystal": ("purple", gem("purple", "#e0b8ff", "#4c1d95")),
    "ruby_crystal": ("pink", gem("#f43f5e", "#ffc0d0", "#9f1239")),
    "titanium": ("gray", [("p", [(14, 60), (32, 22), (70, 14), (88, 50), (74, 84), (28, 86)], "lgray"), ("p", [(32, 22), (70, 14), (60, 46), (38, 50)], "white"),
                          ("p", [(60, 46), (88, 50), (74, 84), (50, 70)], "dgray")]),
    "gold_nugget": ("gold", [("p", [(14, 62), (30, 28), (62, 20), (86, 46), (78, 82), (30, 86)], "gold"), ("p", [(30, 28), (62, 20), (54, 44), (36, 46)], "#fff3b0"),
                             ("p", [(54, 44), (86, 46), (78, 82), (46, 70)], "amber")]),
    "common_ore": ("gray", [("p", [(12, 66), (26, 30), (58, 18), (84, 40), (88, 74), (44, 88)], "dgray"), ("p", [(26, 30), (58, 18), (50, 44), (34, 48)], "gray"),
                            ("p", [(50, 44), (84, 40), (88, 74), (60, 66)], "#2b3544")]),
    "element_shard": ("purple", [("p", [(50, 4), (74, 44), (58, 96), (42, 96), (26, 44)], "purple"), ("p", [(50, 4), (74, 44), (50, 50)], "#e0b8ff"), ("p", [(50, 50), (74, 44), (58, 96)], "#4c1d95")]),
    "organic_matter": ("green", [("p", [(50, 90), (14, 50), (30, 14), (60, 22), (86, 52)], "green"), ("l", [(50, 90), (50, 30)], "#14532d", 4),
                                 ("l", [(50, 62), (30, 44)], "#14532d", 3), ("l", [(50, 52), (70, 38)], "#14532d", 3)]),
    "fiber": ("white", [("l", [(20, 92), (30, 50), (22, 10)], "white", 6), ("l", [(40, 92), (46, 50), (42, 8)], "lgray", 6),
                        ("l", [(60, 92), (58, 50), (66, 10)], "white", 6), ("l", [(80, 92), (72, 50), (82, 12)], "lgray", 6)]),
    "gas_canister": ("amber", [("r", (28, 22, 72, 90), 10, "amber"), ("r", (40, 8, 60, 26), 4, "lgray"), ("r", (28, 44, 72, 64), 2, "dark"), ("e", (44, 48, 56, 60), "gold")]),
    "sample_jar": ("aqua", [("r", (26, 26, 74, 90), 10, "cyan2"), ("r", (22, 12, 78, 28), 5, "lgray"), ("e", (34, 52, 66, 84), "green"), ("l", [(34, 38), (34, 70)], "white", 3)]),
    "coral_sample": ("pink", [("l", [(50, 90), (50, 50), (30, 28)], "pink", 9), ("l", [(50, 50), (72, 26)], "pink", 9), ("l", [(50, 66), (28, 54)], "#fb7185", 8),
                              ("e", (22, 20, 38, 36), "pink"), ("e", (64, 18, 80, 34), "pink"), ("e", (14, 46, 30, 62), "#fb7185")]),
    "seaweed": ("green", [("l", [(30, 94), (22, 66), (38, 44), (26, 14)], "green", 9), ("l", [(52, 94), (62, 62), (48, 38), (60, 8)], "#22c55e", 9), ("l", [(74, 94), (68, 70), (80, 50)], "green", 8)]),
    "organism": ("green", [("e", (14, 24, 86, 88), "green"), ("e", (30, 40, 44, 56), "white"), ("e", (56, 40, 70, 56), "white"), ("e", (35, 45, 41, 53), "dark"), ("e", (61, 45, 67, 53), "dark"),
                           ("l", [(36, 72), (50, 78), (64, 72)], "#14532d", 4)]),
    "dna_sample": ("aqua", [("l", [(28, 6), (72, 36), (28, 64), (72, 94)], "aqua", 7), ("l", [(72, 6), (28, 36), (72, 64), (28, 94)], "purple", 7),
                            ("l", [(38, 22), (62, 22)], "white", 3), ("l", [(38, 78), (62, 78)], "white", 3)]),
    "ancient_relic": ("gold", lantern("gold", "amber", "aqua")),
    "ancient_lantern": ("aqua", lantern("navy2", "lgray", "cyan2")),
    "crystal_relic": ("purple", [("ring", (10, 10, 90, 90), "purple", 6)] + [("p", [(50, 26), (66, 44), (58, 76), (42, 76), (34, 44)], "#c4a5ff"), ("p", [(50, 26), (66, 44), (50, 48), (34, 44)], "white")]),
    "fossil": ("amber", [("a", (12, 12, 88, 88), 20, 340, "amber", 9), ("a", (28, 28, 72, 72), 40, 320, "amber", 8), ("e", (42, 42, 58, 58), "amber"), ("l", [(80, 70), (92, 86)], "amber", 7)]),
    "obsidian_core": ("purple", [("p", [(50, 6), (88, 28), (88, 72), (50, 94), (12, 72), (12, 28)], "#14081f"), ("l", [(50, 6), (50, 50), (88, 72)], "#a06bff", 4), ("l", [(50, 50), (12, 72)], "#a06bff", 4),
                                  ("l", [(12, 28), (50, 50), (88, 28)], "#a06bff", 3)]),
    "data_pod": ("aqua", [("r", (14, 30, 86, 74), 22, "navy2"), ("r", (14, 30, 86, 74), 22, "navy2"), ("e", (24, 40, 44, 64), "aqua"), ("l", [(54, 44), (78, 44)], "cyan2", 5), ("l", [(54, 58), (72, 58)], "cyan2", 5)]),
    "stone_tablet": ("gold", [("p", [(24, 90), (24, 24), (50, 8), (76, 24), (76, 90)], "dgray"), ("l", [(38, 34), (62, 34)], "gold", 4), ("l", [(38, 50), (62, 50)], "gold", 4),
                              ("l", [(38, 66), (56, 66)], "gold", 4)]),
    "relic_fragment": ("amber", [("p", [(16, 70), (40, 14), (86, 40), (70, 86)], "amber"), ("p", [(40, 14), (86, 40), (58, 52)], "#fde68a"), ("l", [(40, 14), (58, 52), (70, 86)], "#92400e", 3)]),
    "relic_orb": ("purple", [("e", (10, 10, 90, 90), "purple"), ("e", (22, 20, 50, 44), "#e0b8ff"), ("ring", (10, 10, 90, 90), "#c4a5ff", 4)]),
    "battery_cell": ("green", [("r", (28, 18, 72, 90), 8, "green"), ("r", (40, 6, 60, 20), 3, "lgray"), ("p", [(54, 36), (40, 58), (50, 58), (46, 78), (62, 52), (52, 52)], "dark")]),
    "oxygen_canister": ("aqua", [("r", (30, 22, 70, 92), 14, "blue"), ("r", (40, 8, 60, 26), 5, "lgray"), ("r", (30, 40, 70, 56), 2, "cyan2"), ("l", [(60, 12), (82, 12)], "lgray", 4)]),
    "repair_kit": ("red", [("r", (10, 28, 90, 84), 9, "red"), ("l", [(34, 28), (34, 18), (66, 18), (66, 28)], "lgray", 5), ("r", (42, 40, 58, 72), 2, "white"), ("r", (30, 50, 70, 62), 2, "white")]),
    "tool_kit": ("amber", [("r", (10, 34, 90, 86), 8, "amber"), ("l", [(34, 34), (34, 20), (66, 20), (66, 34)], "gold", 5), ("l", [(10, 56), (90, 56)], "dark", 4), ("r", (42, 50, 58, 64), 3, "dark")]),
    "signal_flare": ("red", [("r", (40, 36, 60, 94), 5, "red"), ("r", (36, 28, 64, 40), 4, "white"), ("p", [(50, 4), (66, 24), (50, 28), (34, 24)], "amber"), ("p", [(50, 12), (58, 24), (50, 26), (42, 24)], "gold")]),
}

ANOMALIES = {
    "energy_vortex": ("aqua", [("a", (8, 8, 92, 92), 30, 330, "aqua", 7), ("a", (24, 24, 76, 76), 90, 400, "cyan2", 7), ("a", (38, 38, 62, 62), 200, 520, "white", 6)]),
    "gas_vent": ("teal", [("p", [(20, 92), (34, 62), (66, 62), (80, 92)], "dgray"), ("e", (34, 56, 66, 70), "dark"), ("e", (40, 30, 52, 42), "teal"), ("e", (54, 16, 70, 32), "cyan2"), ("e", (46, 4, 56, 14), "teal")]),
    "magnetic_field": ("purple", [("a", (14, 14, 86, 86), 180, 360, "purple", 14), ("l", [(14, 50), (14, 78)], "purple", 14), ("l", [(86, 50), (86, 78)], "purple", 14), ("l", [(14, 70), (14, 78)], "red", 14),
                                  ("l", [(86, 70), (86, 78)], "aqua", 14)]),
    "light_phenomenon": ("amber", [("p", star(50, 50, 46, 14, 8), "gold"), ("e", (34, 34, 66, 66), "white")]),
    "unknown_signal": ("aqua", [("a", (10, 10, 90, 90), 200, 340, "aqua", 6), ("a", (24, 24, 76, 76), 200, 340, "aqua", 6), ("a", (14, 14, 86, 86), 20, 160, "aqua", 6),
                                ("l", [(40, 36), (40, 28), (60, 28), (60, 44), (50, 52), (50, 60)], "white", 7), ("e", (46, 68, 54, 76), "white")]),
    "leviathan": ("blue", [("e", (4, 34, 86, 72), "blue"), ("p", [(8, 52), (0, 30), (20, 40)], "blue"), ("p", [(80, 52), (98, 40), (96, 68)], "navy2"), ("e", (22, 46, 30, 54), "white"),
                           ("l", [(36, 64), (64, 66)], "navy2", 3)]),
}

EQUIPMENT = {
    "lantern_tool": ("amber", lantern()),
    "scanner_tool": ("aqua", [("r", (24, 14, 76, 92), 9, "lgray"), ("r", (32, 22, 68, 56), 4, "dark"), ("ring", (38, 28, 62, 50), "cyan2", 3), ("e", (47, 35, 53, 41), "cyan2"),
                              ("r", (34, 64, 66, 78), 3, "aqua")]),
    "plasma_cutter": ("amber", [("r", (10, 36, 62, 66), 7, "amber"), ("r", (60, 42, 88, 58), 3, "gray"), ("p", [(24, 64), (40, 64), (36, 92), (22, 92)], "dgray"), ("e", (84, 40, 98, 60), "cyan2"),
                                ("p", [(66, 46), (84, 50), (66, 54)], "white")]),
    "thermal_unit": ("aqua", [("r", (30, 26, 70, 92), 12, "blue"), ("r", (38, 12, 62, 30), 5, "lgray"), ("p", [(50, 44), (62, 62), (50, 80), (38, 62)], "amber"), ("p", [(50, 54), (56, 64), (50, 74), (44, 64)], "white")]),
    "acoustic_decoy": ("purple", [("e", (28, 28, 72, 72), "purple"), ("ring", (28, 28, 72, 72), "#c4a5ff", 4), ("a", (14, 14, 86, 86), -45, 45, "#c4a5ff", 5), ("a", (14, 14, 86, 86), 135, 225, "#c4a5ff", 5),
                                  ("a", (2, 2, 98, 98), -40, 40, "#c4a5ff", 5), ("a", (2, 2, 98, 98), 140, 220, "#c4a5ff", 5)]),
    "secure_cargo": ("amber", HUD["cargo"][1] + [("a", (36, 40, 64, 70), 180, 360, "white", 4)]),
    "recall_beacon": ("aqua", [("r", (34, 24, 66, 90), 12, "navy2"), ("ring", (34, 24, 66, 90), "aqua", 4), ("e", (42, 36, 58, 52), "aqua"), ("l", [(50, 6), (50, 24)], "lgray", 4),
                               ("a", (18, 0, 82, 40), 210, 330, "aqua", 4)]),
}

CODEX = {
    "codex_sighted": ("gray", [("ring", (6, 24, 94, 76), "lgray", 6), ("e", (34, 32, 66, 68), "lgray"), ("e", (44, 42, 56, 58), "dark")]),
    "codex_scanned": ("aqua", [("ring", (12, 12, 88, 88), "aqua", 7), ("ring", (28, 28, 72, 72), "cyan2", 4), ("l", [(34, 52), (46, 64), (68, 36)], "white", 8)]),
    "codex_studied": ("purple", [("p", [(14, 20), (14, 76), (46, 82), (46, 28)], "#c4a5ff"), ("ring", (46, 28, 86, 68), "purple", 8), ("l", [(80, 62), (94, 82)], "purple", 9), ("e", (54, 36, 70, 52), "cyan2")]),
    "codex_mastered": ("gold", [("ring", (6, 6, 94, 94), "gold", 6), ("p", star(50, 52, 36, 15), "gold"), ("p", star(50, 52, 20, 8), "white")]),
}

CREATURES = {
    "jellyfish": ("aqua", [("e", (18, 8, 82, 66), "aqua"), ("e", (28, 16, 58, 36), "cyan2"), ("l", [(30, 60), (26, 92)], "cyan2", 5), ("l", [(44, 62), (46, 94)], "cyan2", 5),
                           ("l", [(58, 62), (54, 90)], "cyan2", 5), ("l", [(72, 58), (78, 88)], "cyan2", 5)]),
    "anglerfish": ("purple", fish("#6d28d9", "#4c1d95", extra=[("l", [(60, 30), (68, 8), (86, 12)], "lgray", 3), ("e", (82, 6, 96, 20), "amber"),
                                                              ("p", [(72, 62), (80, 54), (84, 66)], "white")])),
    "reef_shark": ("blue", [("p", [(4, 58), (30, 44), (66, 40), (96, 56), (66, 66), (30, 66)], "#4a6fa5"), ("p", [(46, 42), (58, 14), (66, 42)], "#3b5b8c"), ("p", [(4, 58), (0, 36), (20, 52)], "#3b5b8c"),
                            ("p", [(40, 66), (52, 82), (58, 66)], "#3b5b8c"), ("e", (74, 48, 80, 54), "white")]),
    "manta_ray": ("teal", [("p", [(50, 14), (96, 46), (50, 66), (4, 46)], "teal"), ("p", [(50, 14), (96, 46), (50, 40)], "#5eead4"), ("l", [(50, 66), (50, 96)], "teal", 4), ("e", (36, 36, 44, 44), "white"), ("e", (56, 36, 64, 44), "white")]),
    "coral_crab": ("red", [("e", (24, 36, 76, 74), "#ef4444"), ("l", [(24, 50), (8, 36), (8, 18)], "#ef4444", 7), ("l", [(76, 50), (92, 36), (92, 18)], "#ef4444", 7), ("p", [(0, 6), (16, 6), (8, 22)], "#ef4444"),
                           ("p", [(84, 6), (100, 6), (92, 22)], "#ef4444"), ("l", [(30, 72), (18, 90)], "#b91c1c", 5), ("l", [(50, 74), (50, 94)], "#b91c1c", 5), ("l", [(70, 72), (82, 90)], "#b91c1c", 5),
                           ("e", (36, 28, 44, 38), "white"), ("e", (56, 28, 64, 38), "white")]),
    "tube_worm": ("pink", [("l", [(30, 94), (30, 50)], "lgray", 11), ("l", [(52, 94), (52, 36)], "lgray", 11), ("l", [(74, 94), (74, 56)], "lgray", 11),
                           ("p", [(30, 50), (18, 22), (42, 22)], "pink"), ("p", [(52, 36), (40, 8), (64, 8)], "#fb7185"), ("p", [(74, 56), (62, 30), (86, 30)], "pink")]),
    "alien_fish": ("purple", fish("#8b5cf6", "#ec4899", extra=[("e", (50, 48, 56, 54), "cyan2"), ("e", (36, 44, 42, 50), "cyan2"), ("e", (24, 52, 30, 58), "cyan2")])),
    "coral_guardian": ("amber", [("e", (20, 40, 80, 82), "#d97706"), ("p", [(24, 46), (16, 14), (36, 40)], "#fb923c"), ("p", [(50, 40), (44, 6), (60, 6), (56, 40)], "#fbbf24"), ("p", [(76, 46), (84, 14), (64, 40)], "#fb923c"),
                                 ("e", (34, 54, 44, 64), "white"), ("e", (56, 54, 66, 64), "white"), ("e", (38, 57, 42, 62), "dark"), ("e", (60, 57, 64, 62), "dark")]),
}

ZONES = {
    "zone_shallows": ("aqua", [("e", (30, 6, 70, 46), "gold"), ("l", [(50, 0), (50, 4)], "gold", 3), ("l", [(8, 60), (22, 50), (36, 60), (50, 50), (64, 60), (78, 50), (92, 60)], "aqua", 7),
                               ("l", [(8, 80), (22, 70), (36, 80), (50, 70), (64, 80), (78, 70), (92, 80)], "blue", 7)]),
    "zone_kelp_forest": ("green", [("l", [(24, 94), (16, 66), (30, 44), (20, 12)], "green", 9), ("l", [(50, 94), (60, 62), (44, 36), (56, 6)], "#22c55e", 9), ("l", [(76, 94), (68, 66), (82, 42), (74, 16)], "green", 9)]),
    "zone_twilight_reef": ("purple", [("a", (12, 12, 88, 70), 180, 360, "purple", 1), ("p", [(14, 52), (24, 24), (50, 12), (76, 24), (86, 52)], "purple"), ("l", [(40, 52), (36, 90)], "#c4a5ff", 8), ("l", [(60, 52), (64, 90)], "#c4a5ff", 8),
                                      ("e", (32, 26, 42, 36), "#e0b8ff"), ("e", (58, 30, 66, 38), "#e0b8ff")]),
    "zone_station": ("aqua", dome()),
    "zone_abyss": ("blue", [("e", (8, 8, 92, 92), "#0a1830"), ("ring", (8, 8, 92, 92), "blue", 5), ("e", (30, 34, 70, 66), "#12315c"), ("e", (42, 42, 58, 58), "cyan2"), ("e", (48, 46, 52, 54), "dark")]),
    "zone_lost_ruins": ("gold", [("r", (10, 36, 28, 90), 2, "gold"), ("r", (72, 36, 90, 90), 2, "gold"), ("a", (10, 8, 90, 70), 180, 360, "gold", 14), ("l", [(10, 90), (90, 90)], "amber", 6)]),
    "zone_the_hollow": ("gray", [("a", (8, 8, 92, 92), 20, 340, "lgray", 7), ("a", (24, 24, 76, 76), 60, 380, "gray", 7), ("a", (38, 38, 62, 62), 100, 420, "lgray", 6)]),
    "zone_beyond": ("pink", [("p", star(50, 50, 46, 12, 4), "pink"), ("ring", (26, 26, 74, 74), "purple", 5), ("e", (42, 42, 58, 58), "white")]),
}

WINGS = {
    "wing_power_core": ("amber", [("ring", (10, 10, 90, 90), "amber", 7), ("e", (30, 30, 70, 70), "amber"), ("p", [(54, 34), (40, 54), (50, 54), (46, 68), (62, 46), (52, 46)], "dark")]),
    "wing_sub_dock": ("aqua", sub()),
    "wing_workshop": ("amber", [("p", gear(50, 50, 44, 34, 8), "amber"), ("e", (32, 32, 68, 68), "dark"), ("l", [(38, 62), (62, 38)], "white", 8), ("e", (54, 24, 76, 46), "white"), ("e", (60, 30, 70, 40), "dark")]),
    "wing_research_lab": ("purple", [("p", [(42, 8), (58, 8), (58, 36), (88, 86), (12, 86), (42, 36)], "#c4a5ff"), ("p", [(26, 66), (74, 66), (88, 86), (12, 86)], "purple"), ("e", (40, 70, 50, 80), "white"), ("e", (56, 62, 64, 70), "white")]),
    "wing_observatory": ("blue", [("p", [(8, 70), (26, 34), (86, 20), (92, 40), (30, 62)], "blue"), ("l", [(40, 56), (30, 92)], "lgray", 7), ("l", [(40, 56), (58, 92)], "lgray", 7), ("e", (78, 14, 96, 32), "cyan2")]),
    "wing_aquarium": ("teal", [("r", (8, 14, 92, 86), 8, "navy2"), ("ring", (8, 14, 92, 86), "teal", 5), ("p", [(36, 50), (22, 38), (22, 62)], "amber"), ("e", (34, 40, 66, 60), "amber"), ("e", (58, 46, 64, 52), "dark"), ("e", (70, 66, 78, 74), "cyan2")]),
    "wing_archive": ("gold", [("r", (10, 12, 90, 90), 4, "navy2"), ("l", [(10, 40), (90, 40)], "gold", 4), ("l", [(10, 66), (90, 66)], "gold", 4), ("r", (20, 18, 30, 40), 1, "gold"), ("r", (34, 22, 42, 40), 1, "amber"),
                              ("r", (54, 18, 66, 40), 1, "gold"), ("r", (24, 46, 36, 66), 1, "amber"), ("r", (46, 48, 56, 66), 1, "gold"), ("r", (66, 44, 78, 66), 1, "amber")]),
    "wing_docking_ring": ("aqua", [("a", (8, 8, 92, 92), 10, 80, "aqua", 12), ("a", (8, 8, 92, 92), 100, 170, "aqua", 12), ("a", (8, 8, 92, 92), 190, 260, "aqua", 12), ("a", (8, 8, 92, 92), 280, 350, "aqua", 12),
                                   ("e", (40, 40, 60, 60), "cyan2")]),
}

CLASSES = {
    "sub_scout": ("aqua", sub("aqua", "white")),
    "sub_hauler": ("amber", sub("amber", "white", extra=[("r", (28, 32, 40, 46), 2, "gold"), ("r", (66, 32, 78, 46), 2, "gold")])),
    "sub_surveyor": ("teal", sub("teal", "white", extra=[("a", (36, 0, 66, 24), 200, 340, "cyan2", 3), ("a", (28, -8, 74, 28), 210, 330, "cyan2", 3)])),
    "sub_abyssal": ("red", sub("#b91c1c", "#fca5a5", fin="#450a0a")),
    "sub_multicrew": ("gray", sub("#64748b", "#cbd5e1", fin="#334155") + [("a", (30, 8, 70, 48), 180, 360, "lgray", 1), ("r", (34, 70, 66, 90), 3, "dgray")]),
}

TIERS = {
    "tier_outpost": ("aqua", dome(n=1)),
    "tier_station": ("aqua", dome(n=2)),
    "tier_complex": ("aqua", dome(n=3)),
    "tier_citadel": ("gray", dome("dgray", "gray", 3)),
    "tier_deep_empire": ("gray", dome("dgray", "gray", 3) + [("p", star(50, 18, 12, 5, 5), "gold")]),
}

SETS = {"hud": HUD, "roles": ROLES, "resources": RESOURCES, "anomalies": ANOMALIES, "equipment": EQUIPMENT,
        "codex": CODEX, "creatures": CREATURES, "zones": ZONES, "wings": WINGS, "classes": CLASSES, "tiers": TIERS}


# ----------------------------------------------------------- renderer
def u(v):
    return (25 + v * 0.78) * SS


def U(pts):
    return [(u(x), u(y)) for x, y in pts]


def draw_ops(layer, ops, mono=False):
    d = ImageDraw.Draw(layer)

    def C(name):
        return None if mono else col(name)

    for op in ops:
        k = op[0]
        erase = (len(op) > 2 and op[-1] in ("dark",) and k in ("p", "e", "r")) or (k in ("l", "ring", "a") and op[-2 if k != "l" else 2] == "dark")
        if k == "p":
            c = (0, 0, 0, 0) if (mono and op[2] == "dark") else (col("white") if mono else col(op[2]))
            d.polygon(U(op[1]), fill=c)
        elif k == "e":
            x0, y0, x1, y1 = op[1]
            c = (0, 0, 0, 0) if (mono and op[2] == "dark") else (col("white") if mono else col(op[2]))
            d.ellipse([u(x0), u(y0), u(x1), u(y1)], fill=c)
        elif k == "r":
            x0, y0, x1, y1 = op[1]
            c = (0, 0, 0, 0) if (mono and op[3] == "dark") else (col("white") if mono else col(op[3]))
            d.rounded_rectangle([u(x0), u(y0), u(x1), u(y1)], radius=op[2] * 0.78 * SS, fill=c)
        elif k == "l":
            pts, name, w = op[1], op[2], op[3]
            c = (0, 0, 0, 0) if (mono and name == "dark") else (col("white") if mono else col(name))
            wp = w * 0.78 * SS
            d.line(U(pts), fill=c, width=int(wp), joint="curve")
            for x, y in (pts[0], pts[-1]):
                d.ellipse([u(x) - wp / 2, u(y) - wp / 2, u(x) + wp / 2, u(y) + wp / 2], fill=c)
        elif k == "ring":
            x0, y0, x1, y1 = op[1]
            c = (0, 0, 0, 0) if (mono and op[2] == "dark") else (col("white") if mono else col(op[2]))
            if op[3] > 0:
                d.ellipse([u(x0), u(y0), u(x1), u(y1)], outline=c, width=max(1, int(op[3] * 0.78 * SS)))
        elif k == "a":
            x0, y0, x1, y1 = op[1]
            c = (0, 0, 0, 0) if (mono and op[4] == "dark") else (col("white") if mono else col(op[4]))
            if op[5] > 0:
                d.arc([u(x0), u(y0), u(x1), u(y1)], op[2], op[3], fill=c, width=max(1, int(op[5] * 0.78 * SS)))


def plate(accent):
    W = N * SS
    m = Image.new("L", (W, W), 0)
    ImageDraw.Draw(m).rounded_rectangle([4 * SS, 4 * SS, W - 4 * SS, W - 4 * SS], radius=22 * SS, fill=255)
    t = np.linspace(0, 1, W)[:, None, None]
    top, bot = np.array(hex2rgb("#103060"), float), np.array(hex2rgb("#050e24"), float)
    rgb = top * (1 - t) + bot * t
    arr = np.concatenate([np.broadcast_to(rgb, (W, W, 3)), np.full((W, W, 1), 235.0)], -1)
    base = Image.fromarray(arr.astype(np.uint8), "RGBA")
    base.putalpha(ImageChops.multiply(base.getchannel("A"), m))
    # inner accent glow
    glow = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle([4 * SS, 4 * SS, W - 4 * SS, W - 4 * SS], radius=22 * SS, outline=col(accent, 120), width=10 * SS)
    glow = glow.filter(ImageFilter.GaussianBlur(7 * SS))
    glow.putalpha(ImageChops.multiply(glow.getchannel("A"), m))
    base = Image.alpha_composite(base, glow)
    ring = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(ring).rounded_rectangle([4 * SS, 4 * SS, W - 4 * SS, W - 4 * SS], radius=22 * SS, outline=col(accent, 230), width=int(2 * SS))
    gloss = np.zeros((W, W, 4), dtype=np.uint8)
    yy = np.linspace(0, 1, W)[:, None]
    gloss[..., :3] = 255
    gloss[..., 3] = (np.clip(1 - yy / 0.45, 0, 1) ** 1.5 * 34).astype(np.uint8) * np.ones((1, W), dtype=np.uint8)
    gl_img = Image.fromarray(gloss, "RGBA")
    gl_img.putalpha(ImageChops.multiply(gl_img.getchannel("A"), m))
    base = Image.alpha_composite(base, gl_img)
    bev = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(bev).rounded_rectangle([7 * SS, 7 * SS, W - 7 * SS, W - 7 * SS], radius=19 * SS, outline=(255, 255, 255, 38), width=int(1.2 * SS))
    base = Image.alpha_composite(base, bev)
    return Image.alpha_composite(base, ring)


def shade_glyph(glyph):
    """Give flat vector art volume: top-left key light, vertical gradient, inner edge line."""
    arr = np.asarray(glyph, dtype=np.float64) / 255.0
    a = arr[..., 3]
    W = a.shape[0]
    h = gaussian_filter(a, 2.4 * SS)
    gy, gx = np.gradient(h)
    s = (gx + gy) / math.sqrt(2)
    scale = np.percentile(np.abs(s[a > 0.5]), 98) if (a > 0.5).any() else 1.0
    s = np.clip(s / max(scale, 1e-9), -1, 1)
    yy = np.linspace(0, 1, W)[:, None]
    grad = 1.10 - 0.26 * yy
    rgb = arr[..., :3] * grad[..., None]
    rgb = rgb * (1 + 0.34 * s[..., None]) + np.clip(s, 0, 1)[..., None] * 0.14
    band = a - minimum_filter(a, size=int(1.6 * SS))
    rgb = rgb * (1 - 0.38 * np.clip(band, 0, 1))[..., None]
    spec = np.clip((s - 0.55) / 0.45, 0, 1) * a
    rgb = rgb + spec[..., None] * 0.22
    out = np.dstack([np.clip(rgb, 0, 1), a])
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8), "RGBA")


def render(accent, ops):
    W = N * SS
    glyph = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    draw_ops(glyph, ops)
    glyph = shade_glyph(glyph)
    alpha = glyph.getchannel("A")
    outline = alpha.filter(ImageFilter.MaxFilter(9))
    out = plate(accent)
    gl = Image.new("RGBA", (W, W), col(accent, 150))
    gl.putalpha(alpha.filter(ImageFilter.GaussianBlur(5 * SS)))
    out = Image.alpha_composite(out, gl)
    sh = Image.new("RGBA", (W, W), (0, 0, 0, 150))
    sh.putalpha(ImageChops.offset(alpha, 2 * SS, 4 * SS).filter(ImageFilter.GaussianBlur(3 * SS)).point(lambda v: int(v * 0.6)))
    out = Image.alpha_composite(out, sh)
    ol = Image.new("RGBA", (W, W), col("#030a18", 215))
    ol.putalpha(outline)
    out = Image.alpha_composite(out, ol)
    out = Image.alpha_composite(out, glyph)
    return out.resize((N, N), Image.LANCZOS)


def render_mono(ops):
    W = N * SS
    glyph = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    draw_ops(glyph, ops, mono=True)
    return glyph.resize((N, N), Image.LANCZOS)


def build_all():
    manifest = {}
    for cat, items in SETS.items():
        for name, (accent, ops) in items.items():
            rel = f"{cat}/{name}.png"
            save_img(os.path.join(OUT, rel), render(accent, ops))
            rel_m = f"glyph/{cat}/{name}.png"
            save_img(os.path.join(OUT, rel_m), render_mono(ops))
            manifest[f"{cat}/{name}"] = dict(category=cat, accent=PAL.get(accent, accent), plated=rel, glyph=rel_m, size=[N, N])
    with open(os.path.join(OUT, "_report.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print(len(manifest), "icons")
    return manifest


if __name__ == "__main__":
    build_all()
