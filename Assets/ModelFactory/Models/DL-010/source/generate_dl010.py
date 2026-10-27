"""DL-010 Small wreckage set (6 pieces) - procedural generator. Static environmental props for an existing MVP zone;
not a wreck-dungeon or gameplay system. Past-expedition feel, not horror. Y up, pivot at ground contact (y=0)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("metal_dark", "faded_blue", "corrosion", "mineral")); return m
B = dm.box

panel = mk("DL010_BentPanel")
panel.add("faded_blue", B((2.4, 0.12, 1.7), pos=(0, 0.55, -0.1), rot=(18, 0, 0)))
panel.add("faded_blue", B((2.4, 0.12, 0.9), pos=(0, 0.32, 0.95), rot=(-40, 0, 0)))          # bent flap
panel.add("metal_dark", B((2.5, 0.14, 0.14), pos=(0, 0.72, -0.9), rot=(18, 0, 0)))
panel.add("corrosion", B((0.5, 0.14, 0.4), pos=(-0.8, 0.62, -0.2), rot=(18, 0, 0)))
panel.add("amber_accent", B((0.5, 0.05, 0.2), pos=(0.7, 0.66, -0.35), rot=(18, 0, 0)))
panel.add("metal_dark", B((0.14, 0.45, 0.5), pos=(1.15, 0.2, -0.3)))

frame = mk("DL010_BrokenSupportFrame")
frame.add("metal_dark", B((0.22, 2.4, 0.22), pos=(-1.0, 1.2, 0), rot=(0, 0, 4)))
frame.add("metal_dark", B((0.22, 1.5, 0.22), pos=(1.0, 0.75, 0), rot=(0, 0, -6)))            # snapped
frame.add("faded_blue", B((2.4, 0.2, 0.22), pos=(-0.1, 2.2, 0), rot=(0, 0, 8)))
frame.add("corrosion", B((0.28, 0.3, 0.28), pos=(1.04, 1.55, 0), rot=(0, 20, -20)))          # jagged break
frame.add("metal_dark", B((1.1, 0.16, 0.16), pos=(0.9, 0.2, 0.5), rot=(0, 30, 0)))           # fallen brace
frame.add("mineral", B((0.4, 0.18, 0.3), pos=(-1.0, 0.1, 0.0)))

sensor = mk("DL010_SensorHousing")
sensor.add("metal_dark", dm.cylinder(0.55, 1.1, n=10, axis="y", pos=(0, 0.55, 0), r2=0.48))
sensor.add("faded_blue", dm.cylinder(0.58, 0.18, n=10, axis="y", pos=(0, 0.35, 0)))
sensor.add("corrosion", dm.transform(dm.cylinder(0.50, 0.30, n=10, axis="y"), rot=(18, 0, 6), pos=(0.02, 1.2, 0)))   # tilted broken cap
sensor.add("metal_dark", dm.cylinder(0.10, 0.5, n=6, axis="y", pos=(0.15, 1.5, 0.1)))                                # snapped mast stub
sensor.add("amber_accent", B((0.2, 0.12, 0.05), pos=(0, 0.6, 0.5)))
sensor.add("mineral", dm.blob(0.3, 0.12, 0.3, seed=121, pos=(-0.3, 0.1, 0.3)))

door = mk("DL010_CrackedPressureDoor")
door.add("faded_blue", dm.transform(dm.cylinder(1.1, 0.22, n=14, axis="z"), pos=(-0.18, 1.2, 0), rot=(0, 0, 0)))
door.add("metal_dark", dm.transform(dm.cylinder(1.1, 0.22, n=14, axis="z"), pos=(0.2, 1.1, 0.05), rot=(0, 8, -14)) + [0, 0, 0])
door.add("amber_accent", dm.annulus(0.5, 0.4, 0.1, n=10, axis="z", pos=(-0.18, 1.2, 0.17)))
door.add("corrosion", B((0.12, 2.0, 0.26), pos=(0.0, 1.15, 0.0), rot=(0, 0, 8)))             # crack gap filler
door.add("metal_dark", B((2.5, 0.3, 0.7), pos=(0, 0.15, -0.1)))
door.add("mineral", dm.blob(0.5, 0.15, 0.4, seed=122, pos=(0.9, 0.12, 0.5)))

pipe = mk("DL010_PipeSegment")
pipe.add("metal_dark", dm.cylinder(0.28, 2.2, n=10, axis="x", pos=(0, 0.3, 0)))
pipe.add("faded_blue", dm.cylinder(0.38, 0.22, n=10, axis="x", pos=(-0.9, 0.3, 0)))
pipe.add("faded_blue", dm.cylinder(0.38, 0.22, n=10, axis="x", pos=(0.4, 0.3, 0)))
pipe.add("corrosion", dm.transform(dm.cylinder(0.3, 0.3, n=6, axis="x"), rot=(0, 0, 14), pos=(1.15, 0.33, 0)))   # jagged broken end
pipe.add("mineral", dm.blob(0.3, 0.1, 0.25, seed=123, pos=(0.2, 0.08, 0.35)))

crate = mk("DL010_DamagedCrate")
crate.add("faded_blue", B((1.2, 0.9, 0.9), pos=(0, 0.45, 0), rot=(0, 12, 0)))
crate.add("metal_dark", B((1.26, 0.12, 0.96), pos=(0, 0.06, 0), rot=(0, 12, 0)))
crate.add("metal_dark", B((1.26, 0.12, 0.96), pos=(0, 0.84, 0), rot=(0, 12, 0)))
crate.add("corrosion", B((0.5, 0.5, 0.5), pos=(0.5, 0.78, 0.35), rot=(0, 32, 18)))             # dented / caved corner
crate.add("amber_accent", B((0.3, 0.16, 0.05), pos=(-0.2, 0.55, 0.47), rot=(0, 12, 0)))
crate.add("mineral", dm.blob(0.25, 0.1, 0.22, seed=124, pos=(-0.6, 0.1, 0.6)))

if __name__ == "__main__":
    P = {"bent_panel": panel, "broken_support_frame": frame, "sensor_housing": sensor, "cracked_pressure_door": door, "pipe_segment": pipe, "damaged_crate": crate}
    xs = [-8.0, -4.2, -1.2, 2.3, 5.6, 8.0]
    col = dm.combine("DL010_WreckageSet", [(P[k], (xs[i], 0, 0)) for i, k in enumerate(P)])
    views = [("3/4", 20, 22), ("front", 0, 0), ("top", 0, 90), ("side", -90, 0)]
    print(dm.emit(OUT, dict(id="DL-010", title="Small wreckage set (6 pieces)", source_script="source/generate_dl010.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-010_WRECKAGE_SET.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Each part in parts/ has its pivot at ground contact (y=0). model.glb spaces the six along X."),
        col, parts=P, views=views, px=58, center=(0, 1.0, 0), title="DL-010 wreckage set - software render of the exported geometry", panel=(1000, 560)))
