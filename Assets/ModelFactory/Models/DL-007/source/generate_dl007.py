"""DL-007 Kelp cluster (small / medium / tall) - procedural low-poly generator. Kelp Forest dressing only.
Y up, pivot at the root centre on the seafloor (y=0)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

def cluster(name, fronds, height, seed):
    m = dm.Model(name); dm.std_materials(m, ("kelp_deep", "kelp_mid", "kelp_lime", "kelp_gold", "stone_blue"))
    rng = np.random.default_rng(seed)
    m.add("stone_blue", dm.blob(0.55, 0.22, 0.55, seed=seed, pos=(0, 0.12, 0)))
    for i in range(fronds):
        ang = rng.uniform(0, 2 * math.pi); rad = rng.uniform(0.05, 0.28)
        h = height * rng.uniform(0.75, 1.0); sway = rng.uniform(0.25, 0.6) * (h / 3.0); ph = rng.uniform(0, 6.28)
        steps = 9
        pts = []
        for s in range(steps):
            t = s / (steps - 1)
            pts.append((math.cos(ang) * rad + math.sin(t * 3.0 + ph) * sway * t, 0.15 + h * t,
                        math.sin(ang) * rad + math.cos(t * 2.2 + ph) * sway * 0.6 * t))
        width = [0.05 + 0.02 * (1 - s / (steps - 1)) if s < 2 else 0.30 * (1 - ((s - 1) / (steps - 1)) ** 2.2) + 0.03 for s in range(steps)]
        mat = ("kelp_deep", "kelp_mid", "kelp_mid", "kelp_lime")[i % 4]
        m.add(mat, dm.sweep(pts, width, [0.025] * steps, n=4, hint=(math.sin(ang + 1.0), 0.0, math.cos(ang + 1.0))))
        m.add("kelp_deep", dm.sweep(pts[:5], [0.055, 0.05, 0.045, 0.04, 0.035], n=5))        # thick stipe
        if i % 3 == 0:                                                                       # gas bladder
            p = pts[3]
            m.add("kelp_gold", dm.blob(0.10, 0.13, 0.10, seed=seed + i, rough=0.05, lat=3, lon=6, pos=(p[0], p[1] + 0.05, p[2])))
    return m

if __name__ == "__main__":
    P = {"kelp_small": cluster("DL007_KelpSmall", 5, 2.4, 11), "kelp_medium": cluster("DL007_KelpMedium", 7, 3.8, 12), "kelp_tall": cluster("DL007_KelpTall", 9, 5.8, 13)}
    col = dm.combine("DL007_KelpCluster", [(P[k], (i * 1.8 - 1.8, 0, 0)) for i, k in enumerate(P)])
    views = [("3/4", 30, 12), ("front", 0, 0), ("side", -90, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-007", title="Kelp cluster (small, medium, tall)", source_script="source/generate_dl007.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-007_KELP_CLUSTER.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Each part in parts/ has its pivot at the root centre on the seafloor (y=0). model.glb lays the three out 1.8 m apart along X."),
        col, parts=P, views=views, px=48, center=(0, 2.6, 0), title="DL-007 kelp cluster - software render of the exported geometry"))
