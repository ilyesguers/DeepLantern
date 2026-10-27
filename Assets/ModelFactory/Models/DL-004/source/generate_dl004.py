"""DL-004 Sample canister family (3 variants) - procedural generator. Visual props only; the
sample contents are separate meshes. No inventory/crafting logic. Y up, pivot at geometric centre."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

def mk(name):
    m = dm.Model(name); dm.std_materials(m, ("teal_shell", "titanium", "specimen_violet")); return m

# ---- 1. standard pressure capsule (upright, 0.62 m tall) --------------------
std = mk("DL004_StandardCapsule")
std.add("teal_shell", dm.cylinder(0.22, 0.10, n=12, axis="y", pos=(0, 0.26, 0)))
std.add("teal_shell", dm.cylinder(0.22, 0.10, n=12, axis="y", pos=(0, -0.26, 0)))
std.add("glass_cyan", dm.cylinder(0.17, 0.42, n=12, axis="y"))
std.add("emissive_cyan", dm.cylinder(0.07, 0.28, n=8, axis="y"))             # replaceable sample
for y in (0.19, -0.19):
    std.add("amber_accent", dm.cylinder(0.185, 0.045, n=12, axis="y", pos=(0, y, 0)))  # locking bands
for a in (0, 120, 240):
    std.add("titanium", dm.box((0.05, 0.42, 0.05), pos=(math.sin(math.radians(a)) * 0.185, 0, math.cos(math.radians(a)) * 0.185)))
std.add("graphite_navy", dm.box((0.05, 0.05, 0.26), pos=(0, 0.375, 0)))        # carry handle bar
for dz in (-0.12, 0.12):
    std.add("graphite_navy", dm.box((0.05, 0.10, 0.05), pos=(0, 0.33, dz)))
std.add("hull_offwhite", dm.box((0.16, 0.08, 0.02), pos=(0, -0.26, 0.225)))     # empty label plate

# ---- 2. fragile biological sample (caged sphere) ----------------------------
bio = mk("DL004_FragileBioSample")
sph = dm.loft([(-0.20, 0.05, 0.05), (-0.14, 0.15, 0.15), (0.0, 0.20, 0.20), (0.14, 0.15, 0.15), (0.20, 0.05, 0.05)], n=14, power=2.0)
bio.add("glass_cyan", dm.transform(sph, rot=(-90, 0, 0)))
bio.add("specimen_violet", dm.transform(dm.loft([(-0.10, 0.04, 0.04), (-0.04, 0.09, 0.09), (0.06, 0.10, 0.10), (0.11, 0.05, 0.05)], n=10), rot=(-90, 0, 0)))
for y in (0.215, -0.215):
    bio.add("titanium", dm.cylinder(0.14, 0.05, n=12, axis="y", pos=(0, y, 0)))
for i in range(6):
    a = math.radians(i * 60)
    bio.add("graphite_navy", dm.box((0.04, 0.44, 0.04), pos=(math.sin(a) * 0.205, 0, math.cos(a) * 0.205)))
for i in range(3):
    a = math.radians(i * 120 + 30)
    bio.add("amber_accent", dm.box((0.08, 0.06, 0.08), pos=(math.sin(a) * 0.12, -0.265, math.cos(a) * 0.12)))  # shock mounts
bio.add("graphite_navy", dm.box((0.05, 0.05, 0.22), pos=(0, 0.285, 0)))
bio.add("hull_offwhite", dm.box((0.12, 0.06, 0.02), pos=(0, -0.215, 0.17)))

# ---- 3. rare mineral / specimen vault (hexagonal, squat) -------------------
vault = mk("DL004_MineralVault")
vault.add("teal_shell", dm.cylinder(0.27, 0.34, n=6, axis="y"))
vault.add("graphite_navy", dm.cylinder(0.295, 0.06, n=6, axis="y", pos=(0, 0.19, 0)))
vault.add("graphite_navy", dm.cylinder(0.295, 0.06, n=6, axis="y", pos=(0, -0.19, 0)))
vault.add("glass_cyan", dm.box((0.16, 0.12, 0.05), pos=(0, 0.04, 0.245)))        # reinforced window
vault.add("graphite_navy", dm.box((0.22, 0.18, 0.04), pos=(0, 0.04, 0.235)))
vault.add("emissive_cyan", dm.box((0.04, 0.04, 0.03), pos=(-0.07, -0.10, 0.25)))
vault.add("amber_accent", dm.box((0.04, 0.04, 0.03), pos=(0.07, -0.10, 0.25)))
for a in (60, 180, 300):
    vault.add("amber_accent", dm.box((0.07, 0.08, 0.05), pos=(math.sin(math.radians(a)) * 0.265, 0.19, math.cos(math.radians(a)) * 0.265), rot=(0, a, 0)))
vault.add("hull_offwhite", dm.box((0.16, 0.07, 0.02), pos=(0, -0.13, 0.243)))
vault.add("titanium", dm.box((0.18, 0.04, 0.04), pos=(0, 0.23, 0)))                # top grip

if __name__ == "__main__":
    parts = {"standard_capsule": std, "fragile_bio_sample": bio, "mineral_vault": vault}
    col = dm.combine("DL004_SampleCanisterFamily", [(std, (-0.8, 0.31, 0)), (bio, (0, 0.31, 0)), (vault, (0.8, 0.31, 0))])
    views = [("3/4", 30, 20), ("front", 0, 0), ("top", 0, 90), ("side", -90, 0)]
    print(dm.emit(OUT, dict(id="DL-004", title="Sample canister family (3 variants)", source_script="source/generate_dl004.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-004_SAMPLE_CANISTERS.md (branch assets/model-factory-queue) + GDD audit",
        reference=None, pivot="Each variant in parts/ has its origin at its geometric centre; model.glb places the three side by side at x=-0.8/0/+0.8 with bottoms on y=0."),
        col, parts=parts, views=views, px=250, center=(0, 0.3, 0), title="DL-004 canister family - software render of the exported geometry"))
