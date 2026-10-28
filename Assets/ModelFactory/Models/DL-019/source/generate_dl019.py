"""DL-019 Small non-threatening fauna (3 creatures) - procedural generator. STATIC, UNRIGGED meshes only: no animation,
AI, capture inventory or combat. Material groups (body vs fins/limbs) import as separate MeshParts for later rigging.
Facing +Z, Y up, pivot at the creature's visual centre."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("coral_orange", "coral_pink", "coral_turq", "coral_violet", "emissive_violet", "emissive_teal")); return m

fish = mk("DL019_ReefFish")
fish.add("coral_orange", dm.blob(0.17, 0.20, 0.38, seed=201, rough=0.04, lat=5, lon=10))
fish.add("coral_turq", dm.prism([(-0.30, 0.0), (-0.60, 0.20), (-0.60, -0.20)], 0.04, "zy", pos=(0, 0, 0)))          # tail fin
fish.add("coral_turq", dm.prism([(-0.15, 0.14), (0.15, 0.14), (0.0, 0.34)], 0.04, "zy", pos=(0, 0.04, 0)))          # dorsal fin
for s in (-1, 1):
    fish.add("coral_turq", dm.box((0.04, 0.05, 0.16), pos=(s * 0.19, -0.04, 0.05), rot=(0, 0, 0)))                  # pectoral fins
    fish.add("hull_offwhite", dm.blob(0.045, 0.045, 0.045, seed=202, rough=0, lat=3, lon=6, pos=(s * 0.13, 0.06, 0.28)))
    fish.add("graphite_navy", dm.blob(0.022, 0.022, 0.022, seed=203, rough=0, lat=3, lon=6, pos=(s * 0.15, 0.06, 0.31)))
fish.add("hull_offwhite", dm.box((0.20, 0.05, 0.05), pos=(0, 0.02, 0.05)))                                           # soft stripe

jelly = mk("DL019_Jellyfish")
bell = [(0.0, 0.52, 0.52), (0.14, 0.50, 0.50), (0.30, 0.40, 0.40), (0.42, 0.24, 0.24), (0.48, 0.08, 0.08)]
jelly.add("coral_violet", dm.transform(dm.loft(bell, n=12, cap_start=False), rot=(-90, 0, 0), pos=(0, 0.0, 0)))
jelly.add("emissive_violet", dm.annulus(0.54, 0.46, 0.06, n=12, axis="y", pos=(0, 0.0, 0)))
jelly.add("emissive_violet", dm.blob(0.10, 0.07, 0.10, seed=211, rough=0.0, lat=3, lon=7, pos=(0, 0.36, 0)))
for i in range(8):
    a = math.radians(i * 45)
    x, z = math.sin(a) * 0.38, math.cos(a) * 0.38
    jelly.add("coral_violet", dm.sweep([(x, 0.0, z), (x * 1.05 + 0.03, -0.3, z * 1.05), (x * 0.9, -0.62, z * 0.9 - 0.04), (x * 1.0, -0.9, z)], [0.05, 0.045, 0.04, 0.03], n=5))
for i in range(4):
    a = math.radians(i * 90 + 20)
    jelly.add("emissive_teal", dm.sweep([(math.sin(a) * 0.12, 0.0, math.cos(a) * 0.12), (math.sin(a) * 0.1, -0.35, math.cos(a) * 0.1), (math.sin(a) * 0.14, -0.7, math.cos(a) * 0.14)], [0.07, 0.06, 0.04], n=5))

shrimp = mk("DL019_CleanerShrimp")
segs = [(0.0, 0.0, 0.30, 0.13, "coral_pink"), (0.0, 0.0, 0.14, 0.14, "hull_offwhite"), (0.0, 0.0, -0.02, 0.14, "coral_pink"), (0.0, 0.01, -0.17, 0.12, "hull_offwhite"), (0.0, 0.03, -0.30, 0.10, "coral_pink"), (0.0, 0.06, -0.41, 0.08, "hull_offwhite")]
for (x, y, z, r, mat) in segs:
    shrimp.add(mat, dm.blob(r, r * 0.85, r * 1.15, seed=221 + int(z * 100) % 7, rough=0.03, lat=4, lon=8, pos=(x, y, z)))
shrimp.add("coral_pink", dm.prism([(-0.40, 0.04), (-0.62, 0.14), (-0.62, -0.06)], 0.16, "zy", pos=(0, 0.05, 0)))     # tail fan
for s in (-1, 1):
    shrimp.add("coral_pink", dm.prism([(-0.43, 0.04), (-0.60, 0.10), (-0.60, -0.04)], 0.07, "zy", pos=(s * 0.10, 0.05, 0)))
    shrimp.add("graphite_navy", dm.blob(0.03, 0.03, 0.03, seed=230, rough=0, lat=3, lon=6, pos=(s * 0.08, 0.09, 0.40)))
    shrimp.add("hull_offwhite", dm.sweep([(s * 0.05, 0.10, 0.36), (s * 0.15, 0.20, 0.55), (s * 0.30, 0.18, 0.78)], [0.025, 0.022, 0.018], n=5))   # antennae
    for k, z in enumerate((0.12, 0.0, -0.12)):
        shrimp.add("coral_pink", dm.box((0.05, 0.12, 0.05), pos=(s * 0.12, -0.12, z), rot=(0, 0, s * 20)))                                       # walking legs

if __name__ == "__main__":
    P = {"reef_fish": fish, "jellyfish": jelly, "cleaner_shrimp": shrimp}
    col = dm.combine("DL019_SmallFauna", [(fish, (-1.5, 0.3, 0)), (jelly, (0, 0.9, 0)), (shrimp, (1.4, 0.2, 0))])
    views = [("3/4", 30, 22), ("front", 0, 0), ("side", -90, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-019", title="Small non-threatening fauna (reef fish, jellyfish, cleaner shrimp) - static, unrigged", source_script="source/generate_dl019.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-019_SMALL_FAUNA.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Creature visual centre; facing +Z. UNRIGGED static meshes (no skeleton, no animation). model.glb spaces the three along X."),
        col, parts=P, views=views, px=140, center=(0, 0.4, 0), title="DL-019 fauna (static, unrigged) - software render of the exported geometry", panel=(800, 480)))
