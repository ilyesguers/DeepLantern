"""DL-015 Cave entrance kit (3 pieces + accent cluster) - procedural generator. A small secret/point of interest inside an
existing MVP zone: no new zone, no procedural cave generation, no GPS marker. The opening is left clear (no blocking surface).
Y up, mouth faces +Z, pivot at ground-contact centre (y=0). Only a finished-material preview is provided (no gray blockout)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("stone_blue", "stone_warm", "sediment", "shadow_blue", "emissive_teal", "coral_violet", "coral_pink")); return m
up = lambda t: dm.transform(t, rot=(-90, 0, 0))

mouth = mk("DL015_RockMouth")
for s, seed in ((-1, 141), (1, 142)):
    mouth.add("stone_blue" if s < 0 else "stone_warm", up(dm.rough_loft([(0, 2.4, 2.2), (2.2, 2.1, 2.0), (4.4, 1.8, 1.8), (5.6, 1.7, 1.7)], n=9, seed=seed, rough=0.14)) + [s * 4.3, 0, 0])
pts = dm.arc_points((0, 4.4, 0), 2.9, 1.7, 175, 5, 10)
mouth.add("stone_blue", dm.sweep(pts, [1.5, 1.3, 1.15, 1.05, 1.0, 1.0, 1.05, 1.15, 1.3, 1.5], [1.35, 1.2, 1.05, 0.95, 0.9, 0.9, 0.95, 1.05, 1.2, 1.35], n=9))
mouth.add("sediment", dm.blob(2.4, 0.15, 1.8, seed=143, rough=0.1, lat=3, lon=10, pos=(0, 0.08, 0.6)))        # worn floor path
mouth.add("shadow_blue", dm.box((5.0, 3.2, 0.3), pos=(0, 2.0, -1.9)))                                          # dark back wall seen inside (set back, not blocking)

ledge = mk("DL015_OverhangingLedge")
ledge.add("stone_warm", up(dm.rough_loft([(0, 4.6, 2.2), (0.9, 4.4, 2.0), (1.8, 3.6, 1.6)], n=9, seed=151, rough=0.12)) + [0, 3.0, 0.0])
ledge.add("stone_blue", up(dm.rough_loft([(0, 3.4, 1.8), (1.4, 3.0, 1.5)], n=9, seed=152, rough=0.1)) + [0.4, 1.6, -0.2])
ledge.add("shadow_blue", dm.box((2.4, 1.6, 1.2), pos=(0, 0.8, -0.4)))                                           # support core
ledge.add("emissive_teal", dm.box((2.6, 0.08, 0.12), pos=(0, 2.95, 1.05)))                                       # luminous mineral seam under lip

butt = mk("DL015_SideWallButtress")
for i, (r, h, x) in enumerate([(2.0, 3.2, 0), (1.6, 2.8, 0.9), (1.2, 2.2, -0.8)]):
    butt.add("stone_blue" if i != 1 else "stone_warm", up(dm.rough_loft([(0, r, r * 0.9), (h * 0.5, r * 0.85, r * 0.78), (h, r * 0.55, r * 0.5)], n=8, seed=161 + i, rough=0.14)) + [x, 0, i * 0.7 - 0.4])
butt.add("sediment", dm.blob(2.4, 0.2, 1.8, seed=165, rough=0.1, lat=3, lon=9, pos=(0, 0.1, 0.4)))

accent = mk("DL015_MineralAccent")
for i, (x, z, h, tilt) in enumerate([(0, 0, 0.9, 0), (0.3, 0.1, 0.6, 18), (-0.28, 0.12, 0.7, -20), (0.1, -0.25, 0.5, 8), (-0.1, 0.3, 0.4, -12)]):
    accent.add("emissive_teal", dm.transform(dm.cylinder(0.09, h, n=5, axis="y", r2=0.02), rot=(tilt, i * 30, tilt * 0.6), pos=(x, h * 0.5, z)))
accent.add("stone_blue", dm.blob(0.5, 0.15, 0.45, seed=171, pos=(0, 0.08, 0)))
accent.add("coral_violet", dm.blob(0.14, 0.12, 0.14, seed=172, rough=0.1, lat=3, lon=6, pos=(0.5, 0.1, 0.2)))

if __name__ == "__main__":
    P = {"rock_mouth": mouth, "overhanging_ledge": ledge, "side_wall_buttress": butt, "mineral_accent": accent}
    col = dm.combine("DL015_CaveEntranceKit", [(mouth, (0, 0, 0)), (ledge, (0, 5.1, 0.1)), (butt, (-9.5, 0, 0)), (accent, (3.6, 0, 2.8))])
    views = [("front", 0, 3), ("3/4", 30, 20), ("side", -90, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-015", title="Cave entrance kit (mouth, ledge, buttress, accent)", source_script="source/generate_dl015.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-015_CAVE_ENTRANCE.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Each part in parts/ has its pivot at ground-contact centre (y=0), mouth facing +Z. model.glb shows an illustrative arrangement (ledge raised 5.1 m, buttress 9.5 m to -X), not a verified snap assembly."),
        col, parts=P, views=views, px=26, center=(-2.0, 4.0, 0), title="DL-015 cave entrance kit - software render of the exported geometry", panel=(1000, 560)))
