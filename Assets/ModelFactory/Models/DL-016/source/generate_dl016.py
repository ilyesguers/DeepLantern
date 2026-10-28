"""DL-016 Cable / hose kit (7 pieces) - procedural generator. Static dressing only: no cable physics, no power network.
Hose radius 0.12 m, connector radius 0.17 m (consistent). Pivot: start-point attachment end of each piece."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

R, RC = 0.12, 0.17
def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("titanium",)); m.material("rubber_dark", (0.05, 0.06, 0.08), metallic=0.0, roughness=0.9); return m

def hose(m, pts, ends=True):
    m.add("rubber_dark", dm.sweep(pts, R, n=8))
    if ends:
        for a, b in ((pts[0], pts[1]), (pts[-1], pts[-2])):
            d = np.subtract(a, b); d = d / np.linalg.norm(d)
            c = np.add(a, d * -0.0)
            m.add("titanium", dm.sweep([np.add(a, d * -0.14), np.add(a, d * 0.06)], RC, n=8))                 # connector collar
            m.add("amber_accent", dm.sweep([np.add(a, d * -0.10), np.add(a, d * -0.04)], RC * 1.12, n=8))      # strain-relief band

def line(n, length=2.0, steps=5):
    return [(length * i / (steps - 1), 0.0, 0.0) for i in range(steps)]

straight = mk("DL016_HoseStraight"); hose(straight, [(0.0, 0.2, 0.0), (0.75, 0.2, 0.0), (1.5, 0.2, 0.0), (2.25, 0.2, 0.0), (3.0, 0.2, 0.0)])

bend90 = mk("DL016_Hose90")
pts = [(0.0, 0.2, 0.0), (0.6, 0.2, 0.0)] + [(0.6 + math.sin(math.radians(a)) * 0.7, 0.2, -0.7 + math.cos(math.radians(a)) * 0.7) for a in (0, 30, 60, 90)] + [(1.3, 0.2, 0.7 + 0.0), (1.3, 0.2, 1.3)]
pts = [(0.0, 0.2, 0.0), (0.7, 0.2, 0.0)] + [(0.7 + math.sin(math.radians(a)) * 0.7, 0.2, math.radians(0) + (1 - math.cos(math.radians(a))) * 0.7) for a in (30, 60, 90)] + [(1.4, 0.2, 1.4), (1.4, 0.2, 2.0)]
hose(bend90, pts)

ubend = mk("DL016_HoseU")
pts = [(0.0, 0.2, 0.0), (0.8, 0.2, 0.0)] + [(0.8 + math.sin(math.radians(a)) * 0.6, 0.2, 0.6 - math.cos(math.radians(a)) * 0.6) for a in (45, 90, 135, 180)][:0]
arc = [(0.8 + math.sin(math.radians(a)) * 0.6, 0.2, 0.6 - math.cos(math.radians(a)) * 0.6) for a in (20, 55, 90, 125, 160, 180)]
hose(ubend, [(0.0, 0.2, 0.0), (0.8, 0.2, 0.0)] + arc + [(0.8, 0.2, 1.2), (0.0, 0.2, 1.2)])

coil = mk("DL016_CoiledCable")
cp = []
for i in range(41):
    t = i / 40.0
    a = t * 4 * 2 * math.pi
    cp.append((math.cos(a) * 0.45, 0.14 + t * 0.55, math.sin(a) * 0.45))
coil.add("rubber_dark", dm.sweep(cp, 0.075, n=6))
coil.add("titanium", dm.sweep([(0.45, 0.14, 0.0), (0.45, 0.14, -0.5), (0.45, 0.14, -0.8)], RC, n=8))
coil.add("titanium", dm.sweep([cp[-1], (cp[-1][0] + 0.1, cp[-1][1] + 0.2, cp[-1][2] - 0.4), (cp[-1][0] + 0.15, cp[-1][1] + 0.2, cp[-1][2] - 0.8)], RC * 0.8, n=8))
coil.add("graphite_navy", dm.cylinder(0.55, 0.12, n=12, axis="y", pos=(0, 0.06, 0)))

wall = mk("DL016_WallConnector")                  # attaches to a wall at the back plane (z=0), socket faces +Z
wall.add("graphite_navy", dm.box((0.5, 0.5, 0.08), pos=(0, 0.25, 0.04)))
wall.add("titanium", dm.cylinder(RC * 1.3, 0.22, n=10, axis="z", pos=(0, 0.25, 0.19)))
wall.add("graphite_navy", dm.annulus(RC * 1.05, RC * 0.75, 0.10, n=10, axis="z", pos=(0, 0.25, 0.32)))
wall.add("emissive_cyan", dm.box((0.08, 0.04, 0.03), pos=(0.16, 0.42, 0.09)))
for sx in (-1, 1):
    for sy in (0.08, 0.42):
        wall.add("titanium", dm.cylinder(0.025, 0.04, n=6, axis="z", pos=(sx * 0.19, sy, 0.1)))

coupling = mk("DL016_PressureCoupling")
coupling.add("rubber_dark", dm.cylinder(R, 1.0, n=8, axis="x", pos=(0.5, 0.2, 0)))
coupling.add("titanium", dm.cylinder(RC * 1.15, 0.30, n=10, axis="x", pos=(0.5, 0.2, 0)))
for x in (0.38, 0.62):
    coupling.add("amber_accent", dm.cylinder(RC * 1.25, 0.05, n=10, axis="x", pos=(x, 0.2, 0)))
coupling.add("graphite_navy", dm.box((0.12, 0.05, 0.05), pos=(0.5, 0.2 + RC * 1.2, 0)))

clamp = mk("DL016_CableClamp")
clamp.add("graphite_navy", dm.box((0.34, 0.06, 0.34), pos=(0, 0.03, 0)))
clamp.add("titanium", dm.annulus(0.20, 0.13, 0.14, n=10, axis="z", pos=(0, 0.2, 0)))
clamp.add("graphite_navy", dm.box((0.06, 0.14, 0.16), pos=(0, 0.1, 0)))
clamp.add("amber_accent", dm.box((0.06, 0.06, 0.06), pos=(0, 0.37, 0)))

if __name__ == "__main__":
    P = {"hose_straight": straight, "hose_90_bend": bend90, "hose_u_bend": ubend, "coiled_cable": coil, "wall_connector": wall, "pressure_coupling": coupling, "cable_clamp": clamp}
    pos = [(-6.0, 0, 3.0), (-2.2, 0, 3.0), (-6.0, 0, -1.2), (-2.0, 0, -2.0), (1.8, 0, -1.4), (3.4, 0, 1.0), (5.5, 0, 0.0)]
    pos = [(-6.0, 0, 2.5), (-2.0, 0, 2.5), (1.5, 0, 2.5), (-5.5, 0, -2.0), (-2.0, 0, -2.0), (1.2, 0, -2.0), (3.0, 0, -2.0)]
    col = dm.combine("DL016_CableKit", [(P[k], pos[i]) for i, k in enumerate(P)])
    views = [("3/4", 25, 30), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-016", title="Cable and hose kit (7 pieces)", source_script="source/generate_dl016.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-016_CABLE_KIT.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Hose pieces: start attachment end at the origin, running toward +X (bend/U turn toward +Z), centreline 0.2 m above the floor plane. Wall connector: back plane z=0, socket faces +Z. model.glb spaces the pieces for preview."),
        col, parts=P, views=views, px=48, center=(-1.5, 0.3, 1.0), title="DL-016 cable kit - software render of the exported geometry", panel=(900, 520), cols=1))
