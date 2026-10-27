"""DL-008 Seafloor rock kit (6 pieces) - procedural low-poly generator. Static geological dressing; no terrain system.
Two material families: cool blue-grey and warm mineral stone. Y up, pivot at ground contact (base centre, y=0)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("stone_blue", "stone_warm", "sediment", "shadow_blue")); return m
up = lambda t: dm.transform(t, rot=(-90, 0, 0))

boulder = mk("DL008_Boulder")
boulder.add("stone_blue", dm.blob(1.5, 0.85, 1.3, seed=31, rough=0.16, lat=6, lon=10, pos=(0, 0.7, 0)))
boulder.add("sediment", dm.blob(1.2, 0.12, 1.1, seed=32, rough=0.1, lat=3, lon=10, pos=(0, 0.16, 0)))

slab = mk("DL008_FracturedSlab")
slab.add("stone_blue", dm.transform(up(dm.rough_loft([(0, 1.7, 1.0), (1.3, 1.55, 0.85), (2.1, 1.1, 0.6)], n=7, seed=33, rough=0.14)), rot=(0, 0, -14)) + [0.0, 0.0, 0.0])
slab.add("stone_warm", dm.transform(up(dm.rough_loft([(0, 0.9, 0.7), (0.7, 0.8, 0.6), (1.0, 0.5, 0.4)], n=6, seed=34, rough=0.12)), pos=(1.5, 0, 0.3), rot=(0, 0, 10)))

tall = mk("DL008_TallSplitRock")
tall.add("stone_blue", up(dm.rough_loft([(0, 0.95, 0.8), (1.6, 0.8, 0.7), (3.4, 0.5, 0.45), (4.0, 0.25, 0.25)], n=7, seed=35, rough=0.12)) + [-0.62, 0, 0])
tall.add("stone_blue", up(dm.rough_loft([(0, 0.85, 0.75), (1.4, 0.7, 0.62), (2.6, 0.42, 0.4), (3.0, 0.2, 0.2)], n=7, seed=36, rough=0.12)) + [0.78, 0, 0.1])
tall.add("shadow_blue", dm.box((0.35, 2.0, 0.9), pos=(0.08, 1.0, 0.0)))   # dark crevice between halves

volcanic = mk("DL008_PorousVolcanicStone")
volcanic.add("stone_warm", dm.blob(1.1, 0.8, 1.0, seed=37, rough=0.28, lat=6, lon=11, pos=(0, 0.65, 0)))
rng = np.random.default_rng(38)
for i in range(9):
    a, e = rng.uniform(0, 6.28), rng.uniform(0.1, 1.1)
    p = (math.cos(a) * math.cos(e) * 0.95, 0.65 + math.sin(e) * 0.72, math.sin(a) * math.cos(e) * 0.88)
    volcanic.add("shadow_blue", dm.blob(0.16, 0.12, 0.16, seed=40 + i, rough=0.1, lat=3, lon=6, pos=p))   # pits

shelf = mk("DL008_LayeredSedimentShelf")
for i, (w, d, y, mat) in enumerate([(3.2, 2.0, 0.0, "stone_blue"), (2.8, 1.8, 0.45, "sediment"), (2.4, 1.6, 0.85, "stone_warm"), (1.8, 1.3, 1.2, "stone_blue")]):
    shelf.add(mat, dm.transform(up(dm.rough_loft([(0, w / 2, d / 2), (0.40, w / 2 * 0.96, d / 2 * 0.96)], n=8, seed=50 + i, rough=0.1)), pos=(0.12 * i, y, 0.08 * i)))

scatter = mk("DL008_ScatterCluster")
for i, (x, z, r, mat) in enumerate([(0, 0, 0.45, "stone_blue"), (0.7, 0.3, 0.3, "stone_warm"), (-0.55, 0.4, 0.28, "stone_blue"), (0.2, -0.6, 0.32, "stone_warm"), (-0.4, -0.5, 0.2, "sediment")]):
    scatter.add(mat, dm.blob(r, r * 0.7, r * 0.9, seed=60 + i, rough=0.2, lat=4, lon=7, pos=(x, r * 0.55, z)))

if __name__ == "__main__":
    P = {"boulder": boulder, "fractured_slab": slab, "tall_split_rock": tall, "porous_volcanic": volcanic, "layered_shelf": shelf, "scatter_cluster": scatter}
    xs = [-8.5, -4.2, 0, 4.0, 8.2, 11.4]
    col = dm.combine("DL008_SeafloorRockKit", [(P[k], (xs[i], 0, 0)) for i, k in enumerate(P)])
    views = [("3/4", 25, 20), ("front", 0, 0), ("top", 0, 90), ("side", -90, 0)]
    print(dm.emit(OUT, dict(id="DL-008", title="Seafloor rock kit (6 pieces)", source_script="source/generate_dl008.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-008_SEAFLOOR_ROCKS.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Each part in parts/ has its pivot at ground contact (base centre, y=0). model.glb spaces the six along X."),
        col, parts=P, views=views, px=40, center=(1.3, 1.5, 0), title="DL-008 rock kit - software render of the exported geometry", panel=(1000, 560)))
