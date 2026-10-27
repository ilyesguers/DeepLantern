"""DL-011 Twilight Reef landmark arch - procedural generator. One landmark inside Zone_TwilightReef; not a new zone
or traversal mechanic. Asymmetric supports, curved lintel, coral shelves, a few luminous focal points.
Y up, X across the opening, pivot at the centre of the footprint on the seafloor (y=0). Clear opening ~6 m x 5.5 m."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

m = dm.Model("DL011_TwilightReefArch")
dm.std_materials(m, ("stone_blue", "stone_warm", "coral_pink", "coral_orange", "coral_violet", "coral_turq", "shadow_blue", "emissive_teal", "emissive_violet"))
up = lambda t: dm.transform(t, rot=(-90, 0, 0))

# asymmetric supports
m.add("stone_blue", up(dm.rough_loft([(0, 2.0, 1.7), (2.2, 1.7, 1.45), (4.6, 1.45, 1.3), (6.6, 1.35, 1.2)], n=9, seed=101, rough=0.14)) + [-3.4, 0, 0])
m.add("stone_warm", up(dm.rough_loft([(0, 2.3, 1.9), (1.8, 2.0, 1.7), (4.2, 1.6, 1.4), (5.6, 1.4, 1.25)], n=9, seed=102, rough=0.14)) + [3.6, 0, 0.3])
m.add("stone_blue", dm.blob(3.2, 0.9, 2.4, seed=103, rough=0.18, lat=5, lon=10, pos=(-3.8, 0.5, 0.2)))
m.add("stone_warm", dm.blob(3.4, 1.0, 2.6, seed=104, rough=0.18, lat=5, lon=10, pos=(4.2, 0.55, 0.3)))
# curved lintel (sweep along an uneven arc from left top to right top)
pts = dm.arc_points((0.1, 5.4, 0), 3.6, 2.3, 170, 10, 11)
pts = [(x, y + 0.25 * math.sin(i * 0.9), z + 0.2 * math.cos(i * 0.7)) for i, (x, y, z) in enumerate(pts)]
rad = [1.35, 1.2, 1.05, 0.95, 0.9, 0.88, 0.92, 1.0, 1.12, 1.25, 1.4]
m.add("stone_blue", dm.sweep(pts, rad, [r * 0.85 for r in rad], n=9))
# coral shelves growing on the structure
rng = np.random.default_rng(105)
shelves = [(-3.2, 2.4, 1.2, "coral_pink"), (-2.6, 4.2, 0.95, "coral_violet"), (3.4, 2.0, 1.4, "coral_orange"), (3.0, 3.8, 1.0, "coral_pink"),
           (-0.2, 7.2, 1.0, "coral_turq"), (1.8, 6.6, 0.8, "coral_violet"), (-2.0, 6.5, 0.85, "coral_orange")]
for i, (x, y, r, mat) in enumerate(shelves):
    t = up(dm.rough_loft([(-0.1, r, r * 0.8), (0.12, r * 0.85, r * 0.7)], n=9, seed=110 + i, rough=0.15))
    m.add(mat, dm.transform(t, rot=(rng.uniform(-8, 8), rng.uniform(0, 90), rng.uniform(-10, 10)), pos=(x, y, 1.05 if x < 0.5 else 1.0)))
# luminous focal growths (fixed to the pillars / lintel)
for (x, y, z, mat) in [(-3.0, 3.1, 1.25, "emissive_teal"), (3.5, 4.6, 1.2, "emissive_violet"), (0.9, 7.0, 0.9, "emissive_teal"), (-3.6, 5.1, 1.1, "emissive_violet")]:
    m.add(mat, dm.blob(0.28, 0.34, 0.28, seed=int(abs(x * 10)), rough=0.05, lat=4, lon=7, pos=(x, y, z)))
    m.add("shadow_blue", dm.cylinder(0.12, 0.18, n=6, axis="y", pos=(x, y - 0.3, z)))

if __name__ == "__main__":
    col = m
    views = [("front (opening)", 0, 4), ("3/4", 30, 22), ("side", -90, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-011", title="Twilight Reef landmark arch", source_script="source/generate_dl011.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-011_TWILIGHT_REEF_ARCH.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Centre of the footprint on the seafloor (0,0,0); opening faces +/-Z, spans X."),
        col, views=views, px=40, center=(0.3, 4.0, 0), title="DL-011 Twilight Reef arch - software render of the exported geometry"))
