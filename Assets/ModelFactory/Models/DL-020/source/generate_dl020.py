"""DL-020 Lighting fixture kit (3 fixtures) - procedural generator. Meshes only: no Roblox light objects, no scripts.
Pivot at the mounting interface of each fixture."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("titanium", "emissive_amber", "teal_shell")); return m

def head(m, pos, rot, r=0.28, length=0.45, lens="emissive_amber"):
    """Lamp head along local +Z with lens guard bars. Built at origin, then placed."""
    t = dm.Model("t"); t.materials = m.materials; t.parts = {k: [] for k in m.materials}
    t.add("graphite_navy", dm.cylinder(r, length, n=12, axis="z", pos=(0, 0, -length / 2), r2=r * 0.9))
    for i in range(6):                                                        # heat vent fins
        t.add("titanium", dm.box((r * 2.05, 0.025, 0.04), pos=(0, -r * 0.55 + i * r * 0.22, -0.28)))
    t.add(lens, dm.cylinder(r * 0.82, 0.05, n=12, axis="z", pos=(0, 0, 0.02)))
    t.add("graphite_navy", dm.annulus(r * 1.02, r * 0.88, 0.06, n=12, axis="z", pos=(0, 0, 0.04)))
    for a in (0, 60, 120):                                                    # robust guard bars
        t.add("titanium", dm.box((r * 2.0, 0.035, 0.035), pos=(0, 0, 0.075), rot=(0, 0, a)))
    c = dm.combine("c", [(t, pos, rot)])
    for k, v in c.parts.items():
        m.parts[k] += v

work = mk("DL020_WorkLamp")
work.add("graphite_navy", dm.box((0.45, 0.08, 0.30), pos=(0, 0.04, 0)))                        # clamp base
work.add("titanium", dm.box((0.12, 0.30, 0.10), pos=(0.16, 0.2, 0)))
work.add("graphite_navy", dm.box((0.10, 0.70, 0.10), pos=(0, 0.45, 0), rot=(0, 0, 8)))
work.add("titanium", dm.cylinder(0.08, 0.14, n=8, axis="z", pos=(-0.05, 0.80, 0)))
work.add("graphite_navy", dm.box((0.10, 0.55, 0.10), pos=(-0.2, 1.05, 0), rot=(0, 0, 38)))
work.add("titanium", dm.cylinder(0.075, 0.14, n=8, axis="z", pos=(-0.34, 1.28, 0)))
head(work, (-0.45, 1.25, 0.05), (0, -75, 0))
work.add("amber_accent", dm.box((0.06, 0.08, 0.06), pos=(0, 0.1, 0.16)))

flood = mk("DL020_WallFloodlight")      # back plane z=0, faces +Z
flood.add("graphite_navy", dm.box((0.5, 0.5, 0.08), pos=(0, 0.25, 0.04)))
flood.add("titanium", dm.box((0.08, 0.34, 0.3), pos=(-0.22, 0.25, 0.22)))
flood.add("titanium", dm.box((0.08, 0.34, 0.3), pos=(0.22, 0.25, 0.22)))
head(flood, (0, 0.25, 0.62), (14, 0, 0), r=0.26, length=0.5, lens="emissive_amber")
flood.add("graphite_navy", dm.box((0.14, 0.10, 0.14), pos=(0, 0.02, 0.15)))                      # cable entry
flood.add("amber_accent", dm.box((0.12, 0.05, 0.03), pos=(0.15, 0.45, 0.09)))                    # service access latch

nav = mk("DL020_NavBeacon")
nav.add("graphite_navy", dm.cylinder(0.32, 0.12, n=10, axis="y", pos=(0, 0.06, 0), r2=0.30))
nav.add("teal_shell", dm.cylinder(0.24, 0.30, n=10, axis="y", pos=(0, 0.27, 0), r2=0.22))
nav.add("titanium", dm.cylinder(0.27, 0.06, n=10, axis="y", pos=(0, 0.45, 0)))
nav.add("emissive_cyan", dm.cylinder(0.20, 0.20, n=10, axis="y", pos=(0, 0.58, 0), r2=0.14))        # lens
for i in range(4):
    a = math.radians(i * 90 + 45)
    nav.add("graphite_navy", dm.box((0.05, 0.28, 0.05), pos=(math.sin(a) * 0.21, 0.58, math.cos(a) * 0.21)))   # guard ribs
nav.add("titanium", dm.cylinder(0.24, 0.05, n=10, axis="y", pos=(0, 0.74, 0), r2=0.16))
nav.add("amber_accent", dm.box((0.10, 0.05, 0.05), pos=(0, 0.12, 0.31)))

if __name__ == "__main__":
    P = {"work_lamp": work, "wall_floodlight": flood, "nav_beacon": nav}
    col = dm.combine("DL020_LightingKit", [(work, (-1.0, 0, 0)), (flood, (0.4, 0.6, 0)), (nav, (1.7, 0, 0))])
    views = [("3/4", 30, 18), ("front", 0, 0), ("side", -90, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-020", title="Lighting fixture kit (work lamp, wall floodlight, nav beacon)", source_script="source/generate_dl020.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-020_LIGHTING_KIT.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Work lamp: clamp base centre (y=0). Floodlight: back plane z=0, faces +Z. Nav beacon: base centre (y=0). No light objects included."),
        col, parts=P, views=views, px=110, center=(0.4, 0.9, 0), title="DL-020 lighting kit - software render of the exported geometry", panel=(800, 480)))
