"""DL-018 Research equipment crates (3 cases + separate lid) - procedural generator. Existing cargo/station dressing only:
no inventory, dropper or storage mechanics. Flat stable base, pivot at base centre (y=0)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("titanium", "teal_shell")); return m

def corners(m, w, h, d, c=0.09, mat="graphite_navy"):
    for sx in (-1, 1):
        for sy in (0, 1):
            for sz in (-1, 1):
                m.add(mat, dm.box((c, c, c), pos=(sx * (w / 2 - c / 2 + 0.01), sy * (h - c) + c / 2 if sy == 0 else h - c / 2, sz * (d / 2 - c / 2 + 0.01))))

hard = mk("DL018_HardCase")
hard.add("teal_shell", dm.box((0.8, 0.32, 0.55), pos=(0, 0.16, 0)))
hard.add("graphite_navy", dm.box((0.82, 0.05, 0.57), pos=(0, 0.16, 0)))                                  # seam band
corners(hard, 0.8, 0.32, 0.55, 0.08)
for x in (-0.22, 0.22):
    hard.add("titanium", dm.box((0.10, 0.06, 0.04), pos=(x, 0.17, 0.285)))                                # latches
hard.add("amber_accent", dm.box((0.30, 0.04, 0.05), pos=(0, 0.345, 0)))                                    # handle bar top
for x in (-0.14, 0.14):
    hard.add("graphite_navy", dm.box((0.04, 0.05, 0.05), pos=(x, 0.335, 0)))
hard.add("hull_offwhite", dm.box((0.20, 0.09, 0.02), pos=(0.25, 0.16, -0.285)))                          # blank label recess

crate_body = mk("DL018_SupplyCrateBody")
crate_body.add("graphite_navy", dm.box((1.4, 0.92, 1.0), pos=(0, 0.46, 0)))
for x in (-0.5, 0.0, 0.5):
    crate_body.add("teal_shell", dm.box((0.12, 0.96, 1.04), pos=(x, 0.46, 0)))
for y in (0.15, 0.77):
    crate_body.add("teal_shell", dm.box((1.44, 0.10, 1.04), pos=(0, y, 0)))
corners(crate_body, 1.4, 0.92, 1.0, 0.11)
crate_body.add("amber_accent", dm.box((0.5, 0.06, 0.04), pos=(0, 0.48, 0.52)))
crate_body.add("hull_offwhite", dm.box((0.34, 0.16, 0.02), pos=(-0.25, 0.33, 0.52)))

crate_lid = mk("DL018_SupplyCrateLid")
crate_lid.add("teal_shell", dm.box((1.44, 0.10, 1.04), pos=(0, 0.05, 0)))
crate_lid.add("graphite_navy", dm.box((1.2, 0.05, 0.8), pos=(0, 0.125, 0)))
for x in (-0.45, 0.45):
    crate_lid.add("titanium", dm.box((0.14, 0.06, 0.06), pos=(x, 0.0, 0.53)))
    crate_lid.add("amber_accent", dm.box((0.12, 0.03, 0.03), pos=(x, 0.15, 0.0)))

instr = mk("DL018_InstrumentCase")
instr.add("graphite_navy", dm.box((0.9, 0.34, 0.6), pos=(0, 0.19, 0)))
instr.add("hull_offwhite", dm.box((0.86, 0.10, 0.56), pos=(0, 0.28, 0)))
for x in (-0.38, 0.38):
    for z in (-0.24, 0.24):
        instr.add("amber_accent", dm.box((0.12, 0.05, 0.12), pos=(x, 0.025, z)))                          # shock-isolating feet
for x in (-0.25, 0.25):
    instr.add("titanium", dm.box((0.10, 0.07, 0.04), pos=(x, 0.22, 0.305)))
instr.add("emissive_cyan", dm.box((0.10, 0.03, 0.02), pos=(0, 0.33, 0.30)))                               # status indicator
instr.add("graphite_navy", dm.box((0.28, 0.05, 0.06), pos=(0, 0.38, 0)))
corners(instr, 0.9, 0.36, 0.6, 0.075)

if __name__ == "__main__":
    P = {"hard_case": hard, "supply_crate_body": crate_body, "supply_crate_lid": crate_lid, "instrument_case": instr}
    col = dm.combine("DL018_ResearchCrates", [(hard, (-1.6, 0, 0)), (crate_body, (0, 0, 0)), (crate_lid, (0, 0.92, 0)), (instr, (1.7, 0, 0)), (hard, (-1.6, 0.32, 0))])
    views = [("3/4", 30, 22), ("front", 0, 0), ("top", 0, 90), ("side", -90, 0)]
    print(dm.emit(OUT, dict(id="DL-018", title="Research equipment crates (hard case, supply crate + lid, instrument case)", source_script="source/generate_dl018.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-018_RESEARCH_CRATES.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Each part has its pivot at base centre (y=0); the lid's origin is its bottom centre. model.glb shows a hard case stacked on a second one to the left as a visual-clipping check (not a measured test)."),
        col, parts=P, views=views, px=110, center=(0, 0.6, 0), title="DL-018 crates - software render of the exported geometry", panel=(800, 480)))
