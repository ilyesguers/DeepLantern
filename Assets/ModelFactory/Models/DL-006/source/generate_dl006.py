"""DL-006 Coral family (5 species) - procedural low-poly generator. Static dressing for Shallows / Twilight Reef.
Y up, pivot at seafloor contact (base centre, y=0)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n)
    dm.std_materials(m, ("coral_pink", "coral_orange", "coral_violet", "coral_mint", "coral_turq", "shadow_blue", "emissive_teal"))
    return m

# 1. branching sea fan (flat fan of tapering branches)
fan = mk("DL006_BranchingFan")
fan.add("shadow_blue", dm.blob(0.45, 0.18, 0.40, seed=1, pos=(0, 0.12, 0)))
fan.add("coral_pink", dm.sweep([(0, 0.1, 0), (0, 0.5, 0), (0, 0.9, 0)], [0.12, 0.10, 0.08], n=6))
for i, a in enumerate(np.linspace(-62, 62, 7)):
    r = math.radians(a)
    pts = [(0, 0.9, 0), (math.sin(r) * 0.55, 0.9 + math.cos(r) * 0.55, 0.04 * i % 0.1), (math.sin(r) * 1.15, 0.9 + math.cos(r) * 1.15, 0)]
    fan.add("coral_pink", dm.sweep(pts, [0.08, 0.06, 0.035], n=5, hint=(0, 0, 1)))
    for sgn in (-1, 1):
        r2 = r + sgn * 0.45
        p0 = pts[1]
        fan.add("coral_orange", dm.sweep([p0, (p0[0] + math.sin(r2) * 0.45, p0[1] + math.cos(r2) * 0.45, 0)], [0.05, 0.028], n=5, hint=(0, 0, 1)))

# 2. rounded brain coral
brain = mk("DL006_BrainCoral")
brain.add("shadow_blue", dm.blob(0.85, 0.25, 0.85, seed=2, rough=0.08, pos=(0, 0.2, 0)))
brain.add("coral_mint", dm.blob(0.78, 0.55, 0.78, seed=3, rough=0.10, lat=6, lon=12, pos=(0, 0.55, 0)))
for i in range(6):                      # ridges
    a = i * 60
    brain.add("coral_turq", dm.blob(0.10, 0.28, 0.5, seed=10 + i, rough=0.1, lat=3, lon=6,
                                    pos=(math.sin(math.radians(a)) * 0.38, 0.95, math.cos(math.radians(a)) * 0.38), rot=(0, a, 0)))

# 3. plate coral (stacked tilted plates)
plate = mk("DL006_PlateCoral")
plate.add("shadow_blue", dm.cylinder(0.22, 0.6, n=7, axis="y", pos=(0, 0.3, 0), r2=0.16))
for i, (r, y, tilt, mat) in enumerate([(1.1, 0.45, 6, "coral_violet"), (0.85, 0.80, -9, "coral_pink"), (0.6, 1.10, 8, "coral_violet")]):
    t = dm.rough_loft([(-0.05, r, r), (0.05, r * 0.93, r * 0.93)], n=11, seed=20 + i, rough=0.12)
    plate.add(mat, dm.transform(dm.transform(t, rot=(-90, 0, 0)), rot=(tilt, 20 * i, 0), pos=(0, y, 0)))

# 4. tubular coral cluster
tube = mk("DL006_TubularCoral")
tube.add("shadow_blue", dm.blob(0.7, 0.16, 0.7, seed=4, pos=(0, 0.1, 0)))
for i, (x, z, h, r) in enumerate([(0, 0, 1.4, 0.17), (0.4, 0.1, 1.0, 0.15), (-0.35, 0.2, 1.15, 0.15), (0.1, -0.4, 0.8, 0.13), (-0.2, -0.3, 1.25, 0.14), (0.45, -0.25, 0.6, 0.12)]):
    tube.add("coral_orange", dm.cylinder(r, h, n=8, axis="y", pos=(x, 0.15 + h / 2, z), r2=r * 1.2))
    tube.add("shadow_blue", dm.cylinder(r * 0.7, 0.04, n=8, axis="y", pos=(x, 0.15 + h + 0.005, z)))   # dark opening
    tube.add("coral_pink", dm.annulus(r * 1.25, r * 0.95, 0.06, n=8, axis="y", pos=(x, 0.15 + h - 0.03, z)))

# 5. compact mound coral with polyps
mound = mk("DL006_MoundCoral")
mound.add("shadow_blue", dm.blob(0.65, 0.15, 0.65, seed=5, pos=(0, 0.1, 0)))
mound.add("coral_orange", dm.blob(0.60, 0.50, 0.60, seed=6, rough=0.12, lat=6, lon=11, pos=(0, 0.45, 0)))
rng = np.random.default_rng(7)
for i in range(14):
    a, e = rng.uniform(0, 2 * math.pi), rng.uniform(0.2, 1.2)
    px, py, pz = math.cos(a) * math.cos(e) * 0.56, 0.45 + math.sin(e) * 0.46, math.sin(a) * math.cos(e) * 0.56
    mound.add("emissive_teal" if i % 5 == 0 else "coral_pink", dm.cylinder(0.05, 0.12, n=5, axis="y", pos=(px, py, pz), r2=0.035))

if __name__ == "__main__":
    P = {"branching_fan": fan, "brain_coral": brain, "plate_coral": plate, "tubular_coral": tube, "mound_coral": mound}
    col = dm.combine("DL006_CoralFamily", [(P[k], (i * 2.4 - 4.8, 0, 0)) for i, k in enumerate(P)])
    views = [("3/4", 25, 22), ("front", 0, 0), ("top", 0, 90), ("side", -90, 0)]
    print(dm.emit(OUT, dict(id="DL-006", title="Coral family (5 species)", source_script="source/generate_dl006.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-006_CORAL_FAMILY.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Each part in parts/ has its pivot at seafloor contact (base centre, y=0). model.glb lays the five out 2.4 m apart along X."),
        col, parts=P, views=views, px=46, center=(0, 0.7, 0), title="DL-006 coral family - software render of the exported geometry"))
