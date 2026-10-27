"""DL-005 Research Lab console - procedural low-poly generator (visual prop only).
No UI, scripts or terminal logic. Front (user side) = +Z, screen at the back (-Z). Pivot: floor centre."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

m = dm.Model("DL005_ResearchConsole")
dm.std_materials(m, ("titanium", "emissive_amber"))
SL = 12.0
surf = lambda zl: 0.93 + 0.04 * math.cos(math.radians(SL)) - zl * math.sin(math.radians(SL))

# base + cabinet
m.add("graphite_navy", dm.box((1.30, 0.18, 0.74), pos=(0, 0.09, 0)))
m.add("hull_offwhite", dm.box((1.20, 0.72, 0.60), pos=(0, 0.54, 0)))
# slanted control deck
m.add("graphite_navy", dm.box((1.24, 0.08, 0.56), pos=(0, 0.93, 0.0), rot=(SL, 0, 0)))
# vents + access panel on front
for i in range(5):
    m.add("graphite_navy", dm.box((0.34, 0.025, 0.02), pos=(-0.30, 0.30 + i * 0.07, 0.305)))
m.add("titanium", dm.box((0.34, 0.40, 0.025), pos=(0.30, 0.50, 0.305)))
m.add("amber_accent", dm.box((0.06, 0.04, 0.04), pos=(0.17, 0.50, 0.325)))

# main screen assembly (local coords then tilted back 15 deg)
bez = dm.box((0.82, 0.52, 0.08)); scr = dm.box((0.70, 0.40, 0.02), pos=(0, 0, 0.05))
m.add("graphite_navy", dm.transform(bez, rot=(-15, 0, 0), pos=(-0.05, 1.32, -0.20)))
m.add("emissive_cyan", dm.transform(scr, rot=(-15, 0, 0), pos=(-0.05, 1.32, -0.20)))
for x in (-0.30, 0.20):
    m.add("graphite_navy", dm.box((0.10, 0.42, 0.10), pos=(x, 1.10, -0.22)))
# secondary status panel (right)
m.add("graphite_navy", dm.transform(dm.box((0.30, 0.24, 0.07)), rot=(-15, 0, 0), pos=(0.50, 1.18, -0.20)))
m.add("emissive_cyan", dm.transform(dm.box((0.23, 0.16, 0.02), pos=(0, 0, 0.045)), rot=(-15, 0, 0), pos=(0.50, 1.18, -0.20)))

# control groups on the deck
for i, x in enumerate((-0.52, -0.40, -0.28)):            # guarded switches
    y = surf(0.12) + 0.02
    m.add("graphite_navy", dm.box((0.07, 0.05, 0.07), pos=(x, y, 0.12), rot=(SL, 0, 0)))
    m.add("amber_accent", dm.box((0.085, 0.03, 0.085), pos=(x, y + 0.06, 0.12), rot=(SL, 0, 0)))
for x in (-0.12, 0.0, 0.12):                                # rotary selectors
    y = surf(0.14) + 0.03
    m.add("titanium", dm.cylinder(0.05, 0.06, n=10, axis="y", pos=(x, y, 0.14)))
    m.add("amber_accent", dm.box((0.015, 0.02, 0.05), pos=(x, y + 0.04, 0.125), rot=(SL, 0, 0)))
for i, x in enumerate((-0.52, -0.40, -0.28, -0.16)):        # push buttons
    y = surf(0.02) + 0.03
    m.add("emissive_cyan" if i % 2 else "amber_accent", dm.cylinder(0.04, 0.05, n=8, axis="y", pos=(x, y, 0.02)))

# scanner pad (right) with thin cyan ring
m.add("graphite_navy", dm.box((0.34, 0.03, 0.30), pos=(0.44, surf(0.05) + 0.015, 0.05), rot=(SL, 0, 0)))
m.add("emissive_cyan", dm.annulus(0.13, 0.105, 0.02, n=18, axis="y", pos=(0.44, surf(0.05) + 0.04, 0.05)))

# cable conduit to a floor connector + lamp bar
m.add("graphite_navy", dm.cylinder(0.04, 0.9, n=8, axis="y", pos=(0.50, 0.45, -0.34)))
m.add("titanium", dm.box((0.13, 0.08, 0.13), pos=(0.50, 0.04, -0.34)))
m.add("graphite_navy", dm.box((0.90, 0.05, 0.05), pos=(-0.05, 1.66, -0.28)))
for x in (-0.35, 0.25):
    m.add("graphite_navy", dm.box((0.05, 0.14, 0.05), pos=(x, 1.60, -0.28)))
    m.add("emissive_amber", dm.box((0.12, 0.04, 0.10), pos=(x, 1.53, -0.22)))
m.add("graphite_navy", dm.box((0.05, 0.40, 0.05), pos=(-0.05, 1.47, -0.30)))

if __name__ == "__main__":
    views = [("3/4 front", 30, 22), ("side", 90, 0), ("front", 0, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-005", title="Research Lab console (visual prop)", source_script="source/generate_dl005.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-005_RESEARCH_CONSOLE.md (branch assets/model-factory-queue) + GDD audit",
        reference=None, pivot="Floor centre of the base (0,0,0); user side is +Z."),
        m, views=views, px=160, center=(0, 0.85, 0), title="DL-005 research console - software render of the exported geometry"))
