"""DL-002 MVP modular station kit - procedural low-poly generator (visual props only).
Grid: 1 unit = 4.0 m wide x 3.0 m tall x 0.4 m thick walls. Origin of every wall-type module = bottom centre of the
wall line (x=width centre, y=0, z=wall centreline). Outpost -> Station -> Complex scale only; no post-MVP tiers."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("titanium", "emissive_amber"))
    m.material("navy_frame", (0.08, 0.16, 0.30), metallic=0.4, roughness=0.55)
    return m

W, H, T = 4.0, 3.0, 0.4

def frame(m, w=W, h=H):
    m.add("navy_frame", dm.box((w, 0.2, 0.5), pos=(0, 0.1, 0)))
    m.add("navy_frame", dm.box((w, 0.2, 0.5), pos=(0, h - 0.1, 0)))
    for s in (-1, 1):
        m.add("navy_frame", dm.box((0.2, h - 0.4, 0.5), pos=(s * (w / 2 - 0.1), h / 2, 0)))

def wall_panel(name="wall_panel", w=W):
    m = mk(name); frame(m, w)
    m.add("hull_offwhite", dm.box((w - 0.4, H - 0.4, 0.30), pos=(0, H / 2, 0)))
    m.add("navy_frame", dm.box((w - 0.6, 0.08, 0.36), pos=(0, 1.0, 0)))          # mid trim
    return m

def window_wall():
    m = mk("window_wall"); frame(m)
    m.add("hull_offwhite", dm.box((3.6, 0.8, 0.30), pos=(0, 0.6, 0)))
    m.add("hull_offwhite", dm.box((3.6, 0.5, 0.30), pos=(0, 2.55, 0)))
    for s in (-1, 1):
        m.add("hull_offwhite", dm.box((0.6, 1.3, 0.30), pos=(s * 1.5, 1.65, 0)))
    m.add("glass_cyan", dm.box((2.4, 1.3, 0.06), pos=(0, 1.65, 0)))
    for s in (-1, 1):
        m.add("navy_frame", dm.box((0.14, 1.5, 0.46), pos=(s * 1.27, 1.65, 0)))
    for y in (0.95, 2.35):
        m.add("navy_frame", dm.box((2.68, 0.14, 0.46), pos=(0, y, 0)))
    return m

def corner_wall():
    m = mk("corner_wall")
    a = wall_panel("a", W)
    b = wall_panel("b", W - 0.4)
    c = dm.combine("c", [(a, (0, 0, 0)), (b, (-W / 2 + 0.2, 0, 2.0), (0, 90, 0))])
    m.parts, m.materials = c.parts, c.materials
    m.add("navy_frame", dm.box((0.56, H, 0.56), pos=(-W / 2 + 0.05, H / 2, 0.05)))   # corner post
    m.add("amber_accent", dm.box((0.10, 0.5, 0.60), pos=(-W / 2 + 0.05, 1.4, 0.05)))
    return m

def floor_tile():
    m = mk("floor_tile")
    for s in (-1, 1):
        m.add("graphite_navy", dm.box((1.8, 0.3, 4.0), pos=(s * 1.1, 0.15, 0)))
        m.add("titanium", dm.box((0.12, 0.31, 3.9), pos=(s * 0.27, 0.15, 0)))        # channel rail
    m.add("navy_frame", dm.box((0.4, 0.12, 4.0), pos=(0, 0.06, 0)))                    # service channel floor
    for z in (-1.2, 1.2):
        m.add("emissive_cyan", dm.box((0.2, 0.05, 0.12), pos=(0, 0.14, z)))
    for s in (-1, 1):
        m.add("amber_accent", dm.box((0.10, 0.02, 3.6), pos=(s * 1.9, 0.31, 0)))      # edge safety strips
    return m

def ceiling_beam():
    m = mk("ceiling_beam")
    m.add("navy_frame", dm.box((W, 0.35, 0.5), pos=(0, 0.175, 0)))
    for s in (-1, 1):
        m.add("graphite_navy", dm.box((0.3, 0.45, 0.6), pos=(s * 1.85, 0.225, 0)))
    m.add("emissive_cyan", dm.box((3.0, 0.04, 0.14), pos=(0, -0.01, 0)))               # underside light strip
    return m

def door_frame():
    m = mk("door_frame"); frame(m)
    m.add("hull_offwhite", dm.box((1.3, 2.6, 0.30), pos=(-1.35, 1.5, 0)))
    m.add("hull_offwhite", dm.box((1.3, 2.6, 0.30), pos=(1.35, 1.5, 0)))
    m.add("hull_offwhite", dm.box((1.4, 0.4, 0.30), pos=(0, 2.6, 0)))
    for s in (-1, 1):
        m.add("navy_frame", dm.box((0.16, 2.4, 0.52), pos=(s * 0.78, 1.4, 0)))
        m.add("graphite_navy", dm.box((0.06, 2.3, 0.42), pos=(s * 0.67, 1.4, 0)))      # pressure seal
    m.add("navy_frame", dm.box((1.72, 0.16, 0.52), pos=(0, 2.52, 0)))
    m.add("graphite_navy", dm.box((1.3, 0.06, 0.42), pos=(0, 2.43, 0)))
    m.add("emissive_cyan", dm.box((0.22, 0.08, 0.06), pos=(0, 2.78, 0.19)))
    return m

def hatch():
    m = mk("hatch"); frame(m)
    m.add("hull_offwhite", dm.box((W - 0.4, H - 0.4, 0.30), pos=(0, H / 2, 0)))
    m.add("navy_frame", dm.annulus(0.95, 0.78, 0.50, n=16, axis="z", pos=(0, 1.5, 0)))
    m.add("titanium", dm.cylinder(0.78, 0.30, n=16, axis="z", pos=(0, 1.5, 0.05)))
    m.add("amber_accent", dm.annulus(0.42, 0.33, 0.10, n=14, axis="z", pos=(0, 1.5, 0.28)))   # wheel
    for a in (0, 90):
        m.add("amber_accent", dm.box((0.9, 0.08, 0.08), pos=(0, 1.5, 0.28), rot=(0, 0, a)))
    m.add("titanium", dm.cylinder(0.10, 0.12, n=8, axis="z", pos=(0, 1.5, 0.30)))
    for i in range(4):                                                                   # lock lugs
        a = math.radians(i * 90 + 45)
        m.add("titanium", dm.box((0.14, 0.14, 0.12), pos=(math.cos(a) * 0.86, 1.5 + math.sin(a) * 0.86, 0.26)))
    return m

def railing(corner=False):
    m = mk("railing_corner" if corner else "railing_short")
    def run(length, rot, pos):
        t = dm.Model("t"); t.materials = m.materials; t.parts = {k: [] for k in m.materials}
        for y in (1.0, 0.55):
            t.add("hull_offwhite", dm.box((length, 0.08, 0.08), pos=(0, y, 0)))
        n = int(round(length / 1.0)) + 1
        for i in range(n):
            t.add("navy_frame", dm.box((0.09, 1.0, 0.09), pos=(-length / 2 + i * length / (n - 1), 0.5, 0)))
        t.add("amber_accent", dm.box((0.14, 0.06, 0.14), pos=(-length / 2, 1.04, 0)))
        c = dm.combine("c", [(t, pos, rot)])
        for k, v in c.parts.items():
            m.parts[k] += v
    if corner:
        run(1.6, (0, 0, 0), (0, 0, 0.8)); run(1.6, (0, 90, 0), (-0.8, 0, 0))
    else:
        run(2.0, (0, 0, 0), (0, 0, 0))
    return m

def pipe_bundle():
    m = mk("pipe_bundle")
    for (y, z, mat, r) in [(0.0, 0.0, "navy_frame", 0.14), (0.0, 0.30, "amber_accent", 0.12), (0.26, 0.15, "titanium", 0.12)]:
        m.add(mat, dm.cylinder(r, W, n=10, axis="x", pos=(0, 0.3 + y, z)))
    for x in (-1.4, 0.0, 1.4):
        m.add("graphite_navy", dm.box((0.14, 0.75, 0.55), pos=(x, 0.4, 0.15)))
    return m

def cable_tray():
    m = mk("cable_tray")
    m.add("graphite_navy", dm.box((W, 0.07, 0.55), pos=(0, 0.035, 0)))
    for s in (-1, 1):
        m.add("graphite_navy", dm.box((W, 0.22, 0.06), pos=(0, 0.14, s * 0.245)))
    for z, mat in [(-0.12, "teal_shell"), (0.0, "emissive_cyan"), (0.12, "amber_accent")]:
        if mat not in m.materials:
            m.material("teal_shell", (0.07, 0.27, 0.32), metallic=0.3, roughness=0.6)
        m.add(mat, dm.cylinder(0.05, W - 0.1, n=8, axis="x", pos=(0, 0.13, z)))
    for x in (-1.5, 0.0, 1.5):
        m.add("titanium", dm.box((0.10, 0.34, 0.62), pos=(x, 0.1, 0)))
    return m

def floodlight():
    m = mk("floodlight_bracket")
    m.add("navy_frame", dm.box((0.5, 0.7, 0.10), pos=(0, 0.35, 0)))
    m.add("titanium", dm.box((0.12, 0.12, 0.60), pos=(0, 0.55, 0.35)))
    hous = dm.transform(dm.cylinder(0.24, 0.45, n=12, axis="z"), rot=(20, 0, 0), pos=(0, 0.45, 0.72))
    m.add("graphite_navy", hous)
    m.add("emissive_amber", dm.transform(dm.cylinder(0.19, 0.05, n=12, axis="z", pos=(0, 0, 0.24)), rot=(20, 0, 0), pos=(0, 0.45, 0.72)))
    m.add("amber_accent", dm.box((0.12, 0.10, 0.14), pos=(0, 0.72, 0.5)))
    return m

def vent_unit():
    m = mk("vent_filter_unit")
    m.add("hull_offwhite", dm.box((1.0, 0.8, 0.5), pos=(0, 0.4, 0)))
    for i in range(6):
        m.add("navy_frame", dm.box((0.8, 0.04, 0.04), pos=(0, 0.2 + i * 0.1, 0.27)))
    m.add("titanium", dm.cylinder(0.18, 0.30, n=10, axis="x", pos=(0.62, 0.4, 0)))
    m.add("amber_accent", dm.box((0.10, 0.12, 0.08), pos=(-0.40, 0.7, 0.27)))
    m.add("navy_frame", dm.box((1.1, 0.08, 0.6), pos=(0, 0.04, 0)))
    m.add("emissive_cyan", dm.box((0.10, 0.05, 0.04), pos=(0.38, 0.7, 0.27)))
    return m

def service_panel():
    m = mk("service_access_panel"); frame(m)
    m.add("hull_offwhite", dm.box((W - 0.4, H - 0.4, 0.30), pos=(0, H / 2, 0)))
    m.add("navy_frame", dm.box((1.14, 1.34, 0.36), pos=(0, 1.4, 0)))
    m.add("titanium", dm.box((1.0, 1.2, 0.40), pos=(0, 1.4, 0)))
    m.add("amber_accent", dm.box((0.22, 0.07, 0.08), pos=(0.28, 1.4, 0.22)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add("graphite_navy", dm.box((0.07, 0.07, 0.06), pos=(sx * 0.44, 1.4 + sy * 0.54, 0.22)))
    return m

if __name__ == "__main__":
    P = {"wall_panel": wall_panel(), "window_wall": window_wall(), "corner_wall": corner_wall(), "door_frame": door_frame(),
         "hatch": hatch(), "service_access_panel": service_panel(), "floor_tile": floor_tile(), "ceiling_beam": ceiling_beam(),
         "railing_short": railing(), "railing_corner": railing(True), "pipe_bundle": pipe_bundle(), "cable_tray": cable_tray(),
         "floodlight_bracket": floodlight(), "vent_filter_unit": vent_unit()}
    order = list(P)
    place = []
    for i, k in enumerate(order):
        r, c = divmod(i, 4)
        place.append((P[k], (c * 5.5 - 8.25, 0, r * 4.6 - 6.9)))
    col = dm.combine("DL002_StationKit", place)
    views = [("3/4 layout (grid spacing 5.5 x 4.6 m, not a snapped assembly)", -150, 32), ("front elevation", 0, 0)]
    print(dm.emit(OUT, dict(id="DL-002", title="MVP modular research station kit (14 modules)", source_script="source/generate_dl002.py",
        brief="Assets/ModelFactory/Tasks/DL-002.md + Blender/MODEL_FACTORY/TASKS/DL-002_RESEARCH_STATION_KIT.md (branch assets/model-factory-queue)",
        reference=None, pivot="Grid unit 4.0 m wide, 3.0 m tall, 0.4 m wall. Wall-type modules: origin at bottom centre of the wall line. model.glb is a spaced preview layout of the 14 modules, not an assembly; use parts/*.glb."),
        col, parts=P, views=views, px=33, center=(0, 0.8, 0), title="DL-002 station kit layout - software render of the exported geometry", panel=(1100, 640), cols=1))
