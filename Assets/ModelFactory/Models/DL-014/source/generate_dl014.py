"""DL-014 Submarine docking pad + service arm - procedural low-poly generator (visual props only).
Compact Docking Ring-compatible staging pad for the existing Sub Dock; no launch/matchmaking/social logic.
Y up, floor-contact plane y=0, pad centred on origin, long axis along Z."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("teal_shell", "titanium")); return m

# ---------------- pad ----------------
pad = mk("DL014_DockingPad")
pad.add("graphite_navy", dm.box((6.4, 0.45, 10.4), pos=(0, 0.225, 0)))
for z in (-5.0, 5.0):
    pad.add("amber_accent", dm.box((6.4, 0.03, 0.30), pos=(0, 0.465, z)))
for x in (-1.6, 1.6):
    for z in (-2.7, 2.7):                      # anti-slip inset panels (raised 1.5 cm to avoid z-fighting)
        pad.add("teal_shell", dm.box((2.3, 0.03, 3.8), pos=(x, 0.465, z)))
for x in (-2.8, 2.8):
    for z in (-3.6, 3.6):                      # four guide marks
        pad.add("amber_accent", dm.box((0.22, 0.035, 1.5), pos=(x, 0.468, z)))
pad.add("hull_offwhite", dm.box((0.18, 0.035, 8.6), pos=(0, 0.468, 0)))   # centre line
for z in (-2.2, 2.4):                          # two cradle supports
    pad.add("graphite_navy", dm.box((3.6, 0.30, 1.0), pos=(0, 0.60, z)))
    for s in (-1, 1):
        pad.add("graphite_navy", dm.box((0.45, 0.95, 1.0), pos=(s * 1.45, 1.25, z), rot=(0, 0, -22 * s)))
        pad.add("amber_accent", dm.box((0.30, 0.10, 0.90), pos=(s * 1.28, 1.70, z), rot=(0, 0, -22 * s)))
for x in (-3.0, 3.0):                          # maintenance light posts
    for z in (-4.8, 4.8):
        pad.add("graphite_navy", dm.box((0.26, 0.90, 0.26), pos=(x, 0.90, z)))
        pad.add("emissive_cyan", dm.box((0.30, 0.14, 0.30), pos=(x, 1.42, z)))
for x in (-2.0, 0.0, 2.0):                     # status indicators on the front edge
    pad.add("emissive_cyan", dm.box((0.40, 0.08, 0.06), pos=(x, 0.30, -5.22)))

# ---------------- service arm (pivot: pylon foot centre on the floor) ----------------
arm = mk("DL014_ServiceArm")
arm.add("graphite_navy", dm.box((1.4, 0.15, 1.4), pos=(0, 0.075, 0)))
arm.add("graphite_navy", dm.cylinder(0.40, 1.3, n=10, axis="y", pos=(0, 0.80, 0), r2=0.34))
arm.add("amber_accent", dm.cylinder(0.43, 0.10, n=10, axis="y", pos=(0, 0.35, 0)))
arm.add("titanium", dm.cylinder(0.36, 0.40, n=10, axis="y", pos=(0, 1.65, 0)))        # swivel joint
j = (0.0, 1.55)
def seg(p0, ang, length, thick=0.36):
    a = math.radians(ang)
    c = (p0[0] + math.cos(a) * length / 2, p0[1] + math.sin(a) * length / 2)
    arm.add("hull_offwhite", dm.box((length, thick, thick), pos=(c[0], c[1], 0), rot=(0, 0, ang)))
    return (p0[0] + math.cos(a) * length, p0[1] + math.sin(a) * length)
e1 = seg(j, 25, 1.4)
arm.add("titanium", dm.cylinder(0.27, 0.46, n=10, axis="z", pos=(e1[0], e1[1], 0)))   # elbow
e2 = seg(e1, -35, 1.1, 0.32)
arm.add("titanium", dm.cylinder(0.22, 0.40, n=10, axis="z", pos=(e2[0], e2[1], 0)))   # wrist
arm.add("graphite_navy", dm.cylinder(0.20, 0.50, n=10, axis="x", pos=(e2[0] + 0.25, e2[1], 0)))      # coupler body
arm.add("amber_accent", dm.annulus(0.25, 0.17, 0.08, n=10, axis="x", pos=(e2[0] + 0.52, e2[1], 0)))  # coupler ring
arm.add("emissive_cyan", dm.box((0.16, 0.06, 0.12), pos=(e2[0] + 0.25, e2[1] + 0.22, 0)))
n = 8
for i in range(n):                              # static hose from pylon to coupler
    t0, t1 = i / n, (i + 1) / n
    f = lambda t: (0.45 + (e2[0] + 0.1 - 0.45) * t, 0.9 + 1.0 * math.sin(math.pi * t) * 0.9 + (e2[1] - 0.9) * t, 0.30)
    p, q = f(t0), f(t1)
    ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
    ln = math.hypot(q[0] - p[0], q[1] - p[1]) + 0.02
    arm.add("graphite_navy", dm.box((ln, 0.14, 0.14), pos=((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, 0.30), rot=(0, 0, ang)))
arm.add("emissive_cyan", dm.box((0.20, 0.10, 0.20), pos=(0, 2.0, 0)))                  # maintenance light
arm.add("graphite_navy", dm.box((0.12, 0.30, 0.12), pos=(0, 1.88, 0)))

if __name__ == "__main__":
    col = dm.combine("DL014_DockingPadSet", [(pad, (0, 0, 0)), (arm, (-4.7, 0, 0))])
    views = [("3/4", -145, 25), ("side", -90, 0), ("front", 0, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-014", title="Submarine docking pad + service arm (compact Docking Ring-compatible)", source_script="source/generate_dl014.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-014_DOCKING_PAD.md (branch assets/model-factory-queue) + GDD audit",
        reference="Scout submarine dimensions from Art/VisualReference/02_Submarine_Design.png (cradle spacing matches DL-001 skids at x=+/-1.15)",
        pivot="parts/pad.glb: centre of the floor-contact plane (0,0,0). parts/arm.glb: foot centre on the floor. model.glb places the arm 4.7 m to the -X side of the pad."),
        col, parts={"pad": pad, "arm": arm}, views=views, px=34, center=(-0.9, 1.0, 0), title="DL-014 docking pad + service arm - software render of the exported geometry"))
