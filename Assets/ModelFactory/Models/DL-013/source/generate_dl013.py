"""DL-013 Discovery specimen display - procedural generator. Visual showcase pedestal for the Aquarium/Gallery wing:
no passive income, stat bonus or interaction. The specimen is a separate replaceable object. Y up, pivot at floor centre."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("teal_shell", "titanium", "emissive_violet")); return m

ped = mk("DL013_DisplayPedestal")
ped.add("graphite_navy", dm.cylinder(0.62, 0.16, n=8, axis="y", pos=(0, 0.08, 0), r2=0.58))
ped.add("teal_shell", dm.cylinder(0.50, 0.12, n=8, axis="y", pos=(0, 0.22, 0)))
ped.add("hull_offwhite", dm.cylinder(0.42, 0.55, n=8, axis="y", pos=(0, 0.555, 0), r2=0.38))
ped.add("hull_offwhite", dm.box((0.34, 0.14, 0.03), pos=(0, 0.45, 0.385)))                      # blank label plate
ped.add("graphite_navy", dm.box((0.40, 0.18, 0.015), pos=(0, 0.45, 0.375)))                       # label recess frame
ped.add("titanium", dm.cylinder(0.50, 0.08, n=12, axis="y", pos=(0, 0.87, 0)))
ped.add("emissive_cyan", dm.annulus(0.46, 0.40, 0.04, n=16, axis="y", pos=(0, 0.93, 0)))          # thin inspection ring
ped.add("graphite_navy", dm.cylinder(0.14, 0.12, n=8, axis="y", pos=(0, 0.97, 0)))                # specimen mount
dome = [(0.00, 0.44, 0.44), (0.25, 0.43, 0.43), (0.50, 0.37, 0.37), (0.68, 0.26, 0.26), (0.78, 0.12, 0.12)]
ped.add("glass_cyan", dm.transform(dm.loft(dome, n=14, cap_start=False), rot=(-90, 0, 0), pos=(0, 0.95, 0)))
for i in range(4):
    a = math.radians(i * 90 + 45)
    ped.add("graphite_navy", dm.box((0.06, 0.10, 0.06), pos=(math.sin(a) * 0.47, 0.92, math.cos(a) * 0.47)))

spec = mk("DL013_SpecimenPlaceholder")
for i, (x, z, h, tilt) in enumerate([(0, 0, 0.42, 0), (0.07, 0.04, 0.30, 16), (-0.07, 0.03, 0.34, -18), (0.02, -0.07, 0.22, 10)]):
    spec.add("emissive_violet", dm.transform(dm.cylinder(0.05, h, n=5, axis="y", r2=0.012), rot=(tilt, i * 40, tilt * 0.5), pos=(x, h / 2, z)))
spec.add("graphite_navy", dm.cylinder(0.11, 0.04, n=8, axis="y", pos=(0, 0.02, 0)))

if __name__ == "__main__":
    P = {"display_pedestal": ped, "specimen_placeholder": spec}
    col = dm.combine("DL013_DiscoveryDisplay", [(ped, (0, 0, 0)), (spec, (0, 1.03, 0))])
    views = [("3/4", 30, 20), ("front", 0, 0), ("side", -90, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-013", title="Discovery specimen display (pedestal + replaceable specimen)", source_script="source/generate_dl013.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-013_DISCOVERY_DISPLAY.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Pedestal: floor centre (0,0,0). Specimen placeholder: bottom centre; model.glb seats it on the mount at y=1.03."),
        col, parts=P, views=views, px=150, center=(0, 0.75, 0), title="DL-013 discovery display - software render of the exported geometry"))
