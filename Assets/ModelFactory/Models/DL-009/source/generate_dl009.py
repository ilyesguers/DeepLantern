"""DL-009 Bioluminescent flora (3 assets) - procedural generator. Non-emissive body + restrained emissive core/rim.
Visual dressing only: no bloom/event logic, no particles. Y up, pivot at base centre (y=0)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("flora_body", "flora_violet", "emissive_teal", "emissive_violet", "emissive_amber", "stone_blue")); return m
up = lambda t: dm.transform(t, rot=(-90, 0, 0))

cup = mk("DL009_CupAnemone")
cup.add("stone_blue", dm.blob(0.7, 0.22, 0.7, seed=71, pos=(0, 0.14, 0)))
cup.add("flora_body", up(dm.rough_loft([(0.2, 0.22, 0.22), (0.55, 0.35, 0.35), (0.95, 0.58, 0.58), (1.15, 0.64, 0.64)], n=10, seed=72, rough=0.08)))
cup.add("emissive_teal", dm.annulus(0.66, 0.54, 0.07, n=10, axis="y", pos=(0, 1.15, 0)))          # glowing rim
cup.add("emissive_teal", dm.cylinder(0.30, 0.06, n=10, axis="y", pos=(0, 0.92, 0)))               # core
for i in range(8):                                                                               # short fleshy lobes
    a = math.radians(i * 45)
    cup.add("flora_violet", dm.cylinder(0.07, 0.30, n=5, axis="y", pos=(math.sin(a) * 0.5, 1.28, math.cos(a) * 0.5), r2=0.05))

bulb = mk("DL009_BulbCluster")
bulb.add("stone_blue", dm.blob(0.8, 0.2, 0.7, seed=73, pos=(0, 0.12, 0)))
for i, (x, z, h, r, glow) in enumerate([(0, 0, 1.3, 0.24, "emissive_violet"), (0.38, 0.1, 0.9, 0.2, "emissive_teal"), (-0.35, 0.2, 1.0, 0.21, "emissive_violet"),
                                        (0.1, -0.4, 0.7, 0.17, "emissive_teal"), (-0.15, 0.45, 0.6, 0.16, "emissive_amber")]):
    bulb.add("flora_violet", dm.sweep([(x, 0.2, z), (x + 0.05, 0.2 + h * 0.5, z), (x, 0.2 + h, z)], [0.07, 0.06, 0.05], n=5))
    bulb.add("flora_body", dm.blob(r, r * 1.1, r, seed=80 + i, rough=0.05, lat=4, lon=8, pos=(x, 0.2 + h + r * 0.8, z)))
    bulb.add(glow, dm.blob(r * 0.5, r * 0.55, r * 0.5, seed=90 + i, rough=0.0, lat=3, lon=6, pos=(x, 0.2 + h + r * 1.05, z)))

flower = mk("DL009_GlowingSeaFlower")
flower.add("stone_blue", dm.blob(0.5, 0.16, 0.5, seed=74, pos=(0, 0.1, 0)))
flower.add("flora_body", dm.sweep([(0, 0.1, 0), (0.12, 0.8, 0.05), (0.05, 1.5, 0), (0, 1.9, 0)], [0.07, 0.06, 0.05, 0.05], n=5))
for i in range(6):
    a = i * 60
    petal = dm.transform(dm.box((0.12, 0.05, 0.42), pos=(0, 0, 0.26)), rot=(-25, a, 0), pos=(0, 1.92, 0))
    flower.add("flora_violet" if i % 2 else "flora_body", petal)
flower.add("emissive_teal", dm.cylinder(0.12, 0.10, n=8, axis="y", pos=(0, 1.96, 0)))

if __name__ == "__main__":
    P = {"cup_anemone": cup, "bulb_cluster": bulb, "glowing_sea_flower": flower}
    col = dm.combine("DL009_BioluminescentFlora", [(P[k], (i * 2.2 - 2.2, 0, 0)) for i, k in enumerate(P)])
    views = [("3/4", 25, 20), ("front", 0, 0), ("top", 0, 90), ("side", -90, 0)]
    print(dm.emit(OUT, dict(id="DL-009", title="Bioluminescent flora (3 assets)", source_script="source/generate_dl009.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-009_BIOLUMINESCENT_FLORA.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Each part in parts/ has its pivot at base centre (y=0). model.glb spaces the three 2.2 m apart along X."),
        col, parts=P, views=views, px=52, center=(0, 1.0, 0), title="DL-009 flora - software render of the exported geometry"))
