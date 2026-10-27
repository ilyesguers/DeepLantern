"""DL-003 Static dive / sonar beacon - procedural low-poly generator (visual prop only).
Anchored landmark: no deployment, network, GPS or reward logic. Y up, pivot at bottom centre."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

m = dm.Model("DL003_DiveBeacon")
dm.std_materials(m, ("teal_shell", "titanium"))
T = lambda tris, **k: dm.transform(tris, **k)
up = lambda t: T(t, rot=(-90, 0, 0))  # loft built along +Z -> along +Y

# weighted base + three deployed feet
m.add("graphite_navy", dm.cylinder(0.58, 0.34, n=12, axis="y", pos=(0, 0.17, 0), r2=0.52))
for i in range(3):
    a = i * 120
    r = 0.78
    m.add("graphite_navy", dm.box((0.95, 0.14, 0.28), pos=(math.sin(math.radians(a)) * r, 0.07, math.cos(math.radians(a)) * r), rot=(0, a + 90, 0)))
    m.add("amber_accent", dm.box((0.20, 0.05, 0.30), pos=(math.sin(math.radians(a)) * (r + 0.40), 0.145, math.cos(math.radians(a)) * (r + 0.40)), rot=(0, a + 90, 0)))

# tapered pressure housing (teal) from y=0.34 to 1.50
m.add("teal_shell", T(up(dm.loft([(0.34, 0.50, 0.50), (0.9, 0.44, 0.44), (1.50, 0.37, 0.37)], n=14, power=2.0)), pos=(0, 0, 0)))
for y, r in [(0.62, 0.52), (1.10, 0.46), (1.50, 0.40)]:
    m.add("titanium", dm.cylinder(r, 0.09, n=14, axis="y", pos=(0, y, 0)))
# service hatch + side service ports
m.add("graphite_navy", dm.box((0.34, 0.30, 0.10), pos=(0, 0.88, 0.45)))
m.add("amber_accent", dm.box((0.20, 0.06, 0.06), pos=(0, 0.88, 0.52)))
for s in (-1, 1):
    m.add("titanium", dm.cylinder(0.075, 0.12, n=8, axis="x", pos=(s * 0.46, 0.80, 0)))
    # orange grab handle (two posts + bar)
    for dz in (-0.14, 0.14):
        m.add("amber_accent", dm.box((0.07, 0.07, 0.07), pos=(s * 0.45, 1.05, dz)))
    m.add("amber_accent", dm.box((0.07, 0.07, 0.35), pos=(s * 0.51, 1.05, 0)))

# protective cage: two titanium rings + six ribs
m.add("titanium", dm.cylinder(0.50, 0.07, n=14, axis="y", pos=(0, 1.55, 0)))
m.add("titanium", dm.cylinder(0.50, 0.07, n=14, axis="y", pos=(0, 2.12, 0)))
for i in range(6):
    a = math.radians(i * 60 + 30)
    m.add("graphite_navy", dm.box((0.09, 0.62, 0.09), pos=(math.sin(a) * 0.46, 1.835, math.cos(a) * 0.46)))
# luminous ring (thin accent) inside the cage
m.add("emissive_cyan", dm.annulus(0.42, 0.34, 0.07, n=20, axis="y", pos=(0, 1.835, 0)))
m.add("graphite_navy", dm.cylinder(0.26, 0.3, n=12, axis="y", pos=(0, 1.835, 0)))  # core column holding the ring
# sensor head + puck
m.add("teal_shell", up(dm.loft([(0.0, 0.40, 0.40), (0.14, 0.34, 0.34), (0.26, 0.16, 0.16)], n=14, power=2.0)) + [0, 2.15, 0])
m.add("emissive_cyan", dm.cylinder(0.12, 0.06, n=10, axis="y", pos=(0, 2.44, 0)))
# tether eye
m.add("titanium", dm.annulus(0.15, 0.08, 0.07, n=12, axis="z", pos=(0, 0.45, -0.55)))
m.add("graphite_navy", dm.box((0.10, 0.16, 0.14), pos=(0, 0.45, -0.46)))

if __name__ == "__main__":
    views = [("3/4", -135, 18), ("side", -90, 0), ("front", 180, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-003", title="Static dive / sonar beacon", source_script="source/generate_dl003.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-003_DIVE_BEACON.md (branch assets/model-factory-queue) + GDD audit",
        reference=None, pivot="Bottom centre of the base (0,0,0); flat base on y=0."),
        m, views=views, px=100, center=(0, 1.25, 0), title="DL-003 dive beacon - software render of the exported geometry"))
