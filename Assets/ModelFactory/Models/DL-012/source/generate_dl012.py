"""DL-012 Ancient seafloor relic (clean + partly-buried variants) - procedural generator. A discoverable prop for the existing
Relics & Artifacts/Codex/Archive categories; no new lore, zone or mechanic (a full Lost Ruins area is post-MVP).
Y up, ring faces +Z, pivot at base centre (y=0). Fine runes are NOT modelled (use material masks later)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "Tools"))
import numpy as np  # noqa: E402
import dlmesh as dm  # noqa: E402

def mk(n):
    m = dm.Model(n); dm.std_materials(m, ("relic_stone", "stone_blue", "sediment", "emissive_teal", "metal_dark", "mineral")); return m

def ring(m, mat, cx, cy, r, w, depth, seg, skip, z=0.0, phase=0.0):
    ang = 360.0 / seg
    L = 2 * math.pi * r / seg * 1.04
    for i in range(seg):
        if i in skip:
            continue
        a = math.radians(i * ang + phase)
        m.add(mat, dm.box((L, w, depth), pos=(cx + math.cos(a) * r, cy + math.sin(a) * r, z), rot=(0, 0, math.degrees(a) + 90)))

def build(sink):
    m = mk("DL012_AncientRelic" + ("_Buried" if sink else ""))
    cy = 4.6 - sink
    ring(m, "relic_stone", 0, cy, 4.3, 0.9, 1.0, 24, {3, 4, 13, 14, 15}, z=0.0)
    ring(m, "relic_stone", 0, cy, 2.9, 0.7, 0.8, 18, {8, 9}, z=0.15, phase=8)
    m.add("metal_dark", dm.cylinder(1.5, 0.7, n=12, axis="z", pos=(0, cy, 0.1)))                  # sealed aperture disc
    m.add("emissive_teal", dm.annulus(1.2, 1.0, 0.1, n=16, axis="z", pos=(0, cy, 0.5)))
    m.add("emissive_teal", dm.cylinder(0.28, 0.12, n=8, axis="z", pos=(0, cy, 0.52)))
    for a in (30, 150, 270):                                                                        # seams linking aperture to inner ring
        r = math.radians(a)
        m.add("emissive_teal", dm.box((0.10, 1.3, 0.08), pos=(math.cos(r) * 2.0, cy + math.sin(r) * 2.0, 0.42), rot=(0, 0, a - 90)))
    for a in (45, 105, 200, 300):                                                                   # broken plates between the rings
        r = math.radians(a)
        m.add("stone_blue", dm.box((0.9, 0.5, 0.55), pos=(math.cos(r) * 3.6, cy + math.sin(r) * 3.6, -0.1), rot=(0, 0, a)))
    for s in (-1, 1):                                                                               # support pylons + base block
        m.add("relic_stone", dm.box((1.1, 3.0 - sink, 1.1), pos=(s * 3.0, (3.0 - sink) / 2, -0.1)))
    m.add("relic_stone", dm.box((8.8, 0.7, 1.7), pos=(0, 0.35 if not sink else -0.2, 0)))
    m.add("emissive_teal", dm.box((0.9, 0.06, 0.08), pos=(0, 0.72 if not sink else 0.1, 0.86)))
    if sink:
        m.add("sediment", dm.blob(5.5, 0.9, 2.6, seed=181, rough=0.12, lat=4, lon=12, pos=(0, 0.05, 0.3)))
    return m

if __name__ == "__main__":
    clean, buried = build(0.0), build(1.2)
    col = dm.combine("DL012_AncientRelicSet", [(clean, (-6.0, 0, 0)), (buried, (6.0, 0, 0))])
    views = [("front", 0, 3), ("3/4", 30, 18), ("side", -90, 0), ("top", 0, 90)]
    print(dm.emit(OUT, dict(id="DL-012", title="Ancient seafloor relic (clean + partly buried)", source_script="source/generate_dl012.py",
        brief="Blender/MODEL_FACTORY/TASKS/DL-012_ANCIENT_RELIC.md (branch assets/model-factory-queue) + GDD audit", reference=None,
        pivot="Base centre (0,0,0) for each part; ring faces +Z. model.glb shows clean (x=-6) and buried (x=+6) side by side."),
        col, parts={"relic_clean": clean, "relic_buried": buried}, views=views, px=30, center=(0, 4.0, 0), title="DL-012 ancient relic - software render of the exported geometry", panel=(1000, 560)))
