"""DL-017 Navigation signage kit (5 blank plates) - procedural generator. Diegetic wayfinding only: no GPS markers,
minimap or UI system. Plates are BLANK; text/arrows are meant to be Roblox UI/decals. Wall pieces: back plane z=0, face +Z.
Cyan marks are navigation geometry, not words."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("titanium",)); return m

def framed(m, w, h, d=0.08, f=0.07):
    m.add("graphite_navy", dm.box((w, f, d + 0.03), pos=(0, f / 2, d / 2)))
    m.add("graphite_navy", dm.box((w, f, d + 0.03), pos=(0, h - f / 2, d / 2)))
    for s in (-1, 1):
        m.add("graphite_navy", dm.box((f, h - 2 * f, d + 0.03), pos=(s * (w / 2 - f / 2), h / 2, d / 2)))
    m.add("hull_offwhite", dm.box((w - 2 * f, h - 2 * f, d), pos=(0, h / 2, d / 2)))                      # blank production plate

plaque = mk("DL017_WallPlaque"); framed(plaque, 1.2, 0.6)
plaque.add("amber_accent", dm.box((0.18, 0.06, 0.04), pos=(-0.45, 0.12, 0.10)))
for sx in (-1, 1):
    plaque.add("titanium", dm.cylinder(0.025, 0.04, n=6, axis="z", pos=(sx * 0.52, 0.3, 0.1)))

hang = mk("DL017_HangingDirectional")     # origin at the ceiling attachment, hangs down -Y, face +Z
hang.add("graphite_navy", dm.box((0.9, 0.08, 0.2), pos=(0, 0.04, 0)))
for sx in (-1, 1):
    hang.add("titanium", dm.box((0.05, 0.5, 0.05), pos=(sx * 0.7, -0.25, 0.0)))
    hang.add("graphite_navy", dm.box((0.14, 0.08, 0.14), pos=(sx * 0.7, 0.04, 0)))
sub = mk("x"); framed(sub, 1.8, 0.55)
hang.parts, hang.materials = dm.combine("c", [(sub, (0, -1.05, 0))]).parts, dm.combine("c", [(sub, (0, -1.05, 0))]).materials
for sx in (-1, 1):
    hang.add("titanium", dm.box((0.05, 0.5, 0.05), pos=(sx * 0.7, -0.25, 0.04)))
hang.add("graphite_navy", dm.box((1.6, 0.06, 0.16), pos=(0, 0.03, 0.04)))
hang.add("emissive_cyan", dm.prism([(0.0, 0.0), (0.25, 0.14), (0.25, -0.14)], 0.05, "xy", pos=(0.7, -0.78, 0.07)))   # chevron mark

floor = mk("DL017_FloorRouteMarker")      # low plate, origin at the centre of the floor contact
floor.add("graphite_navy", dm.cylinder(0.5, 0.05, n=12, axis="y", pos=(0, 0.025, 0)))
floor.add("hull_offwhite", dm.cylinder(0.43, 0.02, n=12, axis="y", pos=(0, 0.055, 0)))
for z in (-0.12, 0.12):
    floor.add("emissive_cyan", dm.prism([(-0.22, -0.16), (0.0, 0.0), (-0.22, 0.16), (-0.12, 0.16), (0.1, 0.0), (-0.12, -0.16)][:3], 0.02, "xz", pos=(0.0, 0.075, z)) * 1.0)

hazard = mk("DL017_HazardPanel"); framed(hazard, 1.4, 0.8)
for i in range(6):
    x = -0.55 + i * 0.22
    hazard.add("amber_accent", dm.prism([(-0.07, -0.30), (0.03, -0.30), (0.10, 0.30), (0.0, 0.30)], 0.03, "xy", pos=(x, 0.4, 0.095)))

plate = mk("DL017_EquipmentPlate"); framed(plate, 0.45, 0.28, d=0.05, f=0.04)
plate.add("amber_accent", dm.box((0.08, 0.04, 0.03), pos=(-0.14, 0.07, 0.07)))
for sx in (-1, 1):
    plate.add("titanium", dm.cylinder(0.016, 0.03, n=6, axis="z", pos=(sx * 0.18, 0.14, 0.06)))

if __name__ == "__main__":
    P = {"wall_plaque": plaque, "hanging_directional": hang, "floor_route_marker": floor, "hazard_panel": hazard, "equipment_plate": plate}
    col = dm.combine("DL017_SignageKit", [(plaque, (-3.4, 0.6, 0)), (hang, (-1.0, 2.2, 0)), (floor, (1.0, 0, 0)), (hazard, (2.5, 0, 0)), (plate, (3.9, 0.2, 0))])
    views = [("front", 0, 0), ("3/4", 25, 20)]
    print(dm.emit(OUT, dict(id="DL-017", title="Navigation signage kit (5 blank plates)", source_script="source/generate_dl017.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-017_SIGNAGE_KIT.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Wall pieces: back plane z=0, bottom centre, facing +Z. Hanging sign: ceiling attachment at the origin. Floor marker: centre of floor contact."),
        col, parts=P, views=views, px=100, center=(0.3, 1.0, 0), title="DL-017 signage kit (blank plates, no words) - software render of the exported geometry", panel=(900, 520), cols=1))
