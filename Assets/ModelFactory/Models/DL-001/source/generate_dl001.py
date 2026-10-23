"""DL-001 Scout research submarine - procedural low-poly generator.

Run:  python3 generate_dl001.py   (needs numpy + Pillow; writes next to this folder's parent)
Dimensions follow Art/VisualReference/02_Submarine_Design.png (Scout ~8 m x 4.2 m x 3.1 m).
Visual asset only: no gameplay, controller or stat data. Nose = -Z, up = +Y.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

m = dm.Model("DL001_ScoutSub")
m.material("hull_offwhite", (0.84, 0.87, 0.90), metallic=0.15, roughness=0.55)
m.material("graphite_navy", (0.07, 0.10, 0.17), metallic=0.45, roughness=0.55)
m.material("amber_accent", (0.93, 0.58, 0.10), metallic=0.2, roughness=0.5)
m.material("glass_cyan", (0.30, 0.78, 0.95), metallic=0.0, roughness=0.1, alpha=0.5)
m.material("emissive_cyan", (0.10, 0.55, 0.80), emissive=(0.25, 0.85, 1.0), roughness=0.4)

# ---- main pressure hull (offwhite) -----------------------------------------
HS = [  # z, rx, ry   (nose at -Z)
    (-3.95, 0.55, 0.45), (-3.45, 1.15, 0.85), (-2.55, 1.55, 1.10), (-1.20, 1.70, 1.20),
    (1.00, 1.70, 1.20), (2.55, 1.42, 1.00), (3.35, 1.02, 0.80), (3.80, 0.78, 0.62),
]
zs = [s[0] for s in HS]; rxs = [s[1] for s in HS]; rys = [s[2] for s in HS]


def hull_r(z, grow=1.0):
    return float(np.interp(z, zs, rxs)) * grow, float(np.interp(z, zs, rys)) * grow


m.add("hull_offwhite", dm.loft(HS, n=16, power=2.6))

# dark structural bands around the hull
for z0, z1 in [(-2.05, -1.80), (-0.15, 0.10), (1.75, 2.00), (3.00, 3.18)]:
    a = hull_r(z0, 1.035); b = hull_r(z1, 1.035)
    m.add("graphite_navy", dm.loft([(z0, a[0], a[1]), (z1, b[0], b[1])], n=16, power=2.6))

# ---- keel + skids -----------------------------------------------------------
m.add("graphite_navy", dm.box((1.7, 0.50, 5.2), pos=(0, -1.22, 0.1)))
for x in (-1.15, 1.15):
    m.add("graphite_navy", dm.box((0.20, 0.18, 4.6), pos=(x, -1.62, 0.2)))
    for z in (-1.4, 1.6):
        m.add("graphite_navy", dm.box((0.16, 0.45, 0.22), pos=(x, -1.40, z)))
m.add("amber_accent", dm.box((1.0, 0.06, 1.2), pos=(0, -1.50, -0.5)))  # underside service plate

# ---- cockpit dome (front-top) ----------------------------------------------
dome = [(0.00, 0.98, 0.98), (0.30, 0.92, 0.92), (0.58, 0.74, 0.74), (0.80, 0.46, 0.46), (0.92, 0.18, 0.18)]
dome_t = dm.transform(dm.loft(dome, n=16, power=2.0, cap_start=False), rot=(-90, 0, 0), pos=(0, 0.88, -2.35))
m.add("glass_cyan", dome_t)
m.add("graphite_navy", dm.cylinder(1.06, 0.20, n=16, axis="y", pos=(0, 0.92, -2.35), r2=1.0))  # retaining ring
for x in (-0.72, 0.72):
    m.add("graphite_navy", dm.box((0.12, 0.10, 0.9), pos=(x, 1.50, -2.35), rot=(0, 0, 18 if x > 0 else -18)))
m.add("emissive_cyan", dm.box((0.40, 0.10, 0.10), pos=(0, 1.42, -2.95)))  # dome cockpit light bar

# ---- nose lantern + work lights --------------------------------------------
m.add("graphite_navy", dm.cylinder(0.50, 0.42, n=14, axis="z", pos=(0, -0.12, -3.95), r2=0.55))
m.add("emissive_cyan", dm.cylinder(0.36, 0.08, n=14, axis="z", pos=(0, -0.12, -4.19)))
for x in (-1.0, 1.0):
    m.add("graphite_navy", dm.box((0.38, 0.30, 0.34), pos=(x, 0.05, -3.12)))
    m.add("emissive_cyan", dm.box((0.26, 0.20, 0.06), pos=(x, 0.05, -3.31)))

# ---- side buoyancy / utility pods ------------------------------------------
pod = [(-1.60, 0.20, 0.30), (-1.20, 0.32, 0.46), (1.80, 0.32, 0.46), (2.20, 0.20, 0.34)]
pod_t = dm.transform(dm.loft(pod, n=10, power=3.0), pos=(1.82, -0.18, 0.3))
m.add_mirrored("graphite_navy", pod_t)
m.add_mirrored("amber_accent", dm.box((0.10, 0.07, 1.5), pos=(1.82, 0.31, 0.4)))     # hazard stripe on pod top
m.add_mirrored("graphite_navy", dm.box((0.34, 0.12, 0.22), pos=(1.45, 0.05, -0.95)))  # strut
m.add_mirrored("graphite_navy", dm.box((0.34, 0.12, 0.22), pos=(1.45, 0.05, 1.45)))

# ---- side amber panels, portholes, cargo hatch -----------------------------
for z, h, w in [(-1.00, 0.55, 1.10), (1.45, 0.45, 0.80)]:
    rx, _ = hull_r(z)
    m.add_mirrored("amber_accent", dm.box((0.10, h, w), pos=(rx * 0.985, 0.18, z)))
rx, _ = hull_r(-1.50)
m.add_mirrored("emissive_cyan", dm.cylinder(0.20, 0.10, n=10, axis="x", pos=(rx * 0.97, 0.30, -1.50)))
rx, _ = hull_r(0.55)
m.add_mirrored("graphite_navy", dm.box((0.12, 0.62, 0.78), pos=(rx * 0.99, -0.12, 0.55)))  # cargo hatch frame
m.add_mirrored("hull_offwhite", dm.box((0.14, 0.46, 0.62), pos=(rx * 1.0, -0.12, 0.55)))

# ---- top equipment: hatch, rail, sonar mast --------------------------------
m.add("graphite_navy", dm.cylinder(0.46, 0.14, n=12, axis="y", pos=(0, 1.27, 0.85)))
m.add("amber_accent", dm.cylinder(0.30, 0.06, n=12, axis="y", pos=(0, 1.35, 0.85)))
for x in (-0.55, 0.55):
    m.add("graphite_navy", dm.box((0.10, 0.10, 2.2), pos=(x, 1.28, 0.6)))
m.add("graphite_navy", dm.cylinder(0.07, 0.60, n=8, axis="y", pos=(0, 1.50, 2.05)))
m.add("graphite_navy", dm.box((0.42, 0.14, 0.20), pos=(0, 1.86, 2.05)))
m.add("emissive_cyan", dm.box((0.12, 0.12, 0.12), pos=(0, 1.99, 2.05)))

# ---- tail fins ---------------------------------------------------------------
m.add("graphite_navy", dm.prism([(2.2, 0.0), (3.8, 0.0), (3.7, 0.95), (3.1, 0.95)], 0.16, "zy", pos=(0, 0.95, 0)))
m.add_mirrored("graphite_navy", dm.box((1.25, 0.12, 0.85), pos=(1.45, -0.05, 3.55)))  # horizontal stabilisers

# ---- rear thrusters ----------------------------------------------------------
for x in (-1.05, 1.05):
    m.add("graphite_navy", dm.cylinder(0.56, 1.5, n=12, axis="z", pos=(x, -0.10, 3.45)))
    m.add("graphite_navy", dm.cylinder(0.66, 0.22, n=12, axis="z", pos=(x, -0.10, 4.12), r2=0.72))
    m.add("emissive_cyan", dm.cylinder(0.42, 0.08, n=12, axis="z", pos=(x, -0.10, 4.26)))
    m.add("amber_accent", dm.cylinder(0.58, 0.07, n=12, axis="z", pos=(x, -0.10, 3.20)))
m.add("graphite_navy", dm.box((0.9, 0.25, 0.5), pos=(0, -0.10, 3.45)))  # thruster bridge

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    m.write_glb(os.path.join(OUT, "model.glb"))
    m.write_obj(os.path.join(OUT, "model.obj"), "model.mtl")
    m.write_mtl(os.path.join(OUT, "model.mtl"))
    views = [("3/4 front", -143, 20), ("side", -90, 0), ("front", 180, 0), ("top", 0, 90)]
    dm.render_sheet(m, os.path.join(OUT, "preview.png"),
                    "DL-001 Scout - software render of the exported geometry (flat shading, no textures)",
                    views, px_per_unit=44, center=(0, 0.2, 0))
    dm.write_manifest(m, OUT, dict(
        id="DL-001", title="Scout / research submarine (visual asset)",
        source_script="source/generate_dl001.py", brief="Assets/ModelFactory/Tasks/DL-001.md",
        reference="Art/VisualReference/02_Submarine_Design.png (Scout length 8 m, width ~4.2 m, height 3.1 m)",
        pivot="Model origin (0,0,0) is the hull centreline at mid-length, roughly the vehicle root; not matched to the existing Studio submarine root (unknown)."))
    print(m.stats())
