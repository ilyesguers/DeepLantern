"""dlmesh - tiny dependency-light (numpy + Pillow) low-poly mesh toolkit for the
Deep Lantern Model Factory.

It builds real triangle geometry from primitives (boxes, lofted tubes, prisms),
exports binary glTF (.glb) and Wavefront OBJ/MTL, and renders a software preview
of the exported geometry. It is a build tool only: no gameplay code, no loaders.

Conventions used by Deep Lantern assets:
  * Y is up, the craft's nose / front points toward -Z (Roblox LookVector), +X is right.
  * Units are metres in the file (the Scout design sheet is specified in metres).
"""
import json
import math
import struct

import numpy as np

# ----------------------------------------------------------------------------
# geometry helpers
# ----------------------------------------------------------------------------

def rot_matrix(rx=0.0, ry=0.0, rz=0.0):
    """Euler rotation in degrees, applied X then Y then Z."""
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    mx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    my = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    mz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return mz @ my @ mx


def _orient_outward(tris):
    """Flip triangles that face the centroid so every normal points outward.
    Valid for convex / star-shaped primitives, which is all this kit builds."""
    tris = np.asarray(tris, dtype=np.float64)
    cen = tris.reshape(-1, 3).mean(axis=0)
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    c = tris.mean(axis=1) - cen
    flip = (n * c).sum(axis=1) < 0
    out = tris.copy()
    out[flip] = out[flip][:, [0, 2, 1], :]
    return out


def transform(tris, rot=(0, 0, 0), pos=(0, 0, 0), scale=(1, 1, 1)):
    t = np.asarray(tris, dtype=np.float64) * np.asarray(scale, dtype=np.float64)
    t = t @ rot_matrix(*rot).T + np.asarray(pos, dtype=np.float64)
    return t


def box(size, pos=(0, 0, 0), rot=(0, 0, 0)):
    sx, sy, sz = (s / 2.0 for s in size)
    v = np.array([[-sx, -sy, -sz], [sx, -sy, -sz], [sx, sy, -sz], [-sx, sy, -sz],
                  [-sx, -sy, sz], [sx, -sy, sz], [sx, sy, sz], [-sx, sy, sz]])
    quads = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (3, 2, 6, 7), (0, 3, 7, 4), (1, 2, 6, 5)]
    tris = []
    for a, b, c, d in quads:
        tris += [[v[a], v[b], v[c]], [v[a], v[c], v[d]]]
    return transform(_orient_outward(tris), rot, pos)


def loft(sections, n=12, power=2.0, cap_start=True, cap_end=True):
    """Lofted tube along local +Z.
    sections: list of (z, rx, ry[, cx, cy]) - a super-ellipse of n points per section.
    power 2 = ellipse, larger = boxier (blocky Roblox look)."""
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    c, s = np.cos(ang), np.sin(ang)
    ex = 2.0 / power
    px = np.sign(c) * np.abs(c) ** ex
    py = np.sign(s) * np.abs(s) ** ex
    rings = []
    for sec in sections:
        z, rx, ry = sec[0], sec[1], sec[2]
        cx = sec[3] if len(sec) > 3 else 0.0
        cy = sec[4] if len(sec) > 4 else 0.0
        rings.append(np.stack([cx + px * rx, cy + py * ry, np.full(n, z)], axis=1))
    tris = []
    for i in range(len(rings) - 1):
        a, b = rings[i], rings[i + 1]
        for k in range(n):
            k2 = (k + 1) % n
            tris += [[a[k], a[k2], b[k2]], [a[k], b[k2], b[k]]]
    if cap_start:
        ctr = rings[0].mean(axis=0)
        for k in range(n):
            tris.append([ctr, rings[0][(k + 1) % n], rings[0][k]])
    if cap_end:
        ctr = rings[-1].mean(axis=0)
        for k in range(n):
            tris.append([ctr, rings[-1][k], rings[-1][(k + 1) % n]])
    return _orient_outward(tris)


def cylinder(r, length, n=12, axis="z", pos=(0, 0, 0), r2=None):
    """Capped cylinder / frustum centred on pos. axis in x|y|z."""
    r2 = r if r2 is None else r2
    t = loft([(-length / 2, r, r), (length / 2, r2, r2)], n=n)
    if axis == "x":
        t = transform(t, rot=(0, 90, 0))
    elif axis == "y":
        t = transform(t, rot=(-90, 0, 0))
    return transform(t, pos=pos)


def prism(poly2d, depth, plane="zy", pos=(0, 0, 0)):
    """Extrude a convex 2D polygon. plane 'zy' = profile in (z,y) extruded along x;
    'xz' = profile in (x,z) extruded along y; 'xy' = profile in (x,y) extruded along z."""
    pts = np.asarray(poly2d, dtype=np.float64)
    h = depth / 2.0
    ring0, ring1 = [], []
    for p in pts:
        if plane == "zy":
            ring0.append((-h, p[1], p[0])); ring1.append((h, p[1], p[0]))
        elif plane == "xz":
            ring0.append((p[0], -h, p[1])); ring1.append((p[0], h, p[1]))
        else:
            ring0.append((p[0], p[1], -h)); ring1.append((p[0], p[1], h))
    ring0, ring1 = np.array(ring0), np.array(ring1)
    m = len(pts)
    tris = []
    for k in range(m):
        k2 = (k + 1) % m
        tris += [[ring0[k], ring0[k2], ring1[k2]], [ring0[k], ring1[k2], ring1[k]]]
    for ring in (ring0, ring1):
        c = ring.mean(axis=0)
        for k in range(m):
            tris.append([c, ring[k], ring[(k + 1) % m]])
    return transform(_orient_outward(tris), pos=pos)


def mirror_x(tris):
    """Mirror across the YZ plane (fixes winding)."""
    t = np.asarray(tris, dtype=np.float64).copy()
    t[..., 0] *= -1
    return t[:, [0, 2, 1], :]


# ----------------------------------------------------------------------------
# model container, export, validation
# ----------------------------------------------------------------------------

class Model:
    def __init__(self, name):
        self.name = name
        self.materials = {}   # key -> dict(color=(r,g,b,a), emissive=(r,g,b)|None, metallic, roughness)
        self.parts = {}       # material key -> list of (n,3,3)

    def material(self, key, color, emissive=None, metallic=0.1, roughness=0.6, alpha=1.0):
        self.materials[key] = dict(color=(*color, alpha), emissive=emissive, metallic=metallic,
                                   roughness=roughness)
        self.parts.setdefault(key, [])

    def add(self, key, tris):
        if key not in self.materials:
            raise KeyError(key)
        self.parts[key].append(np.asarray(tris, dtype=np.float64))

    def add_mirrored(self, key, tris):
        """Add tris and their X-mirror (for left/right symmetric parts)."""
        self.add(key, tris)
        self.add(key, mirror_x(tris))

    def mesh(self, key):
        lst = self.parts[key]
        return np.concatenate(lst, axis=0) if lst else np.zeros((0, 3, 3))

    def stats(self):
        allt = np.concatenate([self.mesh(k) for k in self.parts if len(self.parts[k])], axis=0)
        v = allt.reshape(-1, 3)
        return dict(triangles=int(len(allt)),
                    triangles_per_material={k: int(len(self.mesh(k))) for k in self.parts},
                    bounds_min=[round(float(x), 4) for x in v.min(axis=0)],
                    bounds_max=[round(float(x), 4) for x in v.max(axis=0)],
                    size=[round(float(x), 4) for x in (v.max(axis=0) - v.min(axis=0))])

    # -- glTF ----------------------------------------------------------------
    def write_glb(self, path):
        bin_chunks, views, accessors, meshes, nodes, mats = [], [], [], [], [], []
        offset = 0

        def push(data, target):
            nonlocal offset
            pad = (-len(data)) % 4
            views.append(dict(buffer=0, byteOffset=offset, byteLength=len(data), target=target))
            bin_chunks.append(data + b"\0" * pad)
            offset += len(data) + pad
            return len(views) - 1

        keys = [k for k in self.parts if len(self.parts[k])]
        for mi, key in enumerate(keys):
            m = self.materials[key]
            tris = self.mesh(key).astype(np.float32)
            nrm = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]).astype(np.float64)
            ln = np.linalg.norm(nrm, axis=1, keepdims=True)
            nrm = np.where(ln > 1e-12, nrm / np.maximum(ln, 1e-12), np.array([0, 1, 0.0]))
            pos = tris.reshape(-1, 3)
            nor = np.repeat(nrm, 3, axis=0).astype(np.float32)
            idx = np.arange(len(pos), dtype=np.uint32)
            vp = push(pos.tobytes(), 34962)
            vn = push(nor.tobytes(), 34962)
            vi = push(idx.tobytes(), 34963)
            a0 = len(accessors)
            accessors.append(dict(bufferView=vp, componentType=5126, count=len(pos), type="VEC3",
                                  min=[float(x) for x in pos.min(axis=0)],
                                  max=[float(x) for x in pos.max(axis=0)]))
            accessors.append(dict(bufferView=vn, componentType=5126, count=len(nor), type="VEC3"))
            accessors.append(dict(bufferView=vi, componentType=5125, count=len(idx), type="SCALAR"))
            mat = dict(name=key, pbrMetallicRoughness=dict(
                baseColorFactor=[float(c) for c in m["color"]],
                metallicFactor=float(m["metallic"]), roughnessFactor=float(m["roughness"])),
                doubleSided=True)
            if m["emissive"] is not None:
                mat["emissiveFactor"] = [float(c) for c in m["emissive"]]
            if m["color"][3] < 0.999:
                mat["alphaMode"] = "BLEND"
            mats.append(mat)
            meshes.append(dict(name=f"{self.name}_{key}", primitives=[dict(
                attributes=dict(POSITION=a0, NORMAL=a0 + 1), indices=a0 + 2, material=mi, mode=4)]))
            nodes.append(dict(name=f"{self.name}_{key}", mesh=mi))
        gltf = dict(asset=dict(version="2.0", generator="Deep Lantern dlmesh.py (procedural, no AI)"),
                    scene=0, scenes=[dict(nodes=[len(nodes)])],
                    nodes=nodes + [dict(name=self.name, children=list(range(len(nodes))))],
                    meshes=meshes, materials=mats, accessors=accessors, bufferViews=views,
                    buffers=[dict(byteLength=offset)])
        js = json.dumps(gltf, separators=(",", ":")).encode()
        js += b" " * ((-len(js)) % 4)
        binb = b"".join(bin_chunks)
        total = 12 + 8 + len(js) + 8 + len(binb)
        with open(path, "wb") as f:
            f.write(struct.pack("<4sII", b"glTF", 2, total))
            f.write(struct.pack("<I4s", len(js), b"JSON") + js)
            f.write(struct.pack("<I4s", len(binb), b"BIN\0") + binb)

    # -- OBJ -----------------------------------------------------------------
    def write_obj(self, obj_path, mtl_name):
        lines = [f"# {self.name} - Deep Lantern dlmesh.py (procedural geometry)", f"mtllib {mtl_name}"]
        vbase = 1
        for key in self.parts:
            tris = self.mesh(key)
            if not len(tris):
                continue
            lines += [f"o {self.name}_{key}", f"usemtl {key}"]
            for t in tris:
                for p in t:
                    lines.append("v %.5f %.5f %.5f" % tuple(p))
            for i in range(len(tris)):
                b = vbase + i * 3
                lines.append(f"f {b} {b + 1} {b + 2}")
            vbase += len(tris) * 3
        open(obj_path, "w").write("\n".join(lines) + "\n")

    def write_mtl(self, mtl_path):
        out = []
        for key, m in self.materials.items():
            c = m["color"]
            out += [f"newmtl {key}", "Kd %.4f %.4f %.4f" % c[:3], "d %.3f" % c[3]]
            if m["emissive"] is not None:
                out.append("Ke %.4f %.4f %.4f" % tuple(m["emissive"]))
            out.append("")
        open(mtl_path, "w").write("\n".join(out))


def read_glb_stats(path):
    """Independently re-read a .glb and return what is actually in the file."""
    d = open(path, "rb").read()
    magic, ver, length = struct.unpack("<4sII", d[:12])
    assert magic == b"glTF" and ver == 2 and length == len(d), "bad GLB header"
    jl, jt = struct.unpack("<I4s", d[12:20])
    gltf = json.loads(d[20:20 + jl])
    bo = 20 + jl
    bl, bt = struct.unpack("<I4s", d[bo:bo + 8])
    binb = d[bo + 8:bo + 8 + bl]
    tri = 0
    mins, maxs = [], []
    finite = True
    for mesh in gltf["meshes"]:
        for prim in mesh["primitives"]:
            acc = gltf["accessors"][prim["attributes"]["POSITION"]]
            view = gltf["bufferViews"][acc["bufferView"]]
            arr = np.frombuffer(binb, dtype=np.float32, count=acc["count"] * 3,
                                offset=view["byteOffset"]).reshape(-1, 3)
            finite &= bool(np.isfinite(arr).all())
            mins.append(arr.min(axis=0)); maxs.append(arr.max(axis=0))
            tri += gltf["accessors"][prim["indices"]]["count"] // 3
    mn, mx = np.min(mins, axis=0), np.max(maxs, axis=0)
    return dict(file_bytes=len(d), meshes=len(gltf["meshes"]), materials=len(gltf["materials"]),
                triangles=tri, all_finite=finite,
                bounds_min=[round(float(x), 4) for x in mn], bounds_max=[round(float(x), 4) for x in mx])


# ----------------------------------------------------------------------------
# software preview renderer (orthographic z-buffer, flat shading)
# ----------------------------------------------------------------------------

def _view_matrix(yaw, pitch):
    return rot_matrix(rx=pitch) @ rot_matrix(ry=yaw)


def render_view(model, yaw, pitch, W, H, px_per_unit, ss=2, center=(0, 0, 0)):
    R = _view_matrix(yaw, pitch)
    Ws, Hs = W * ss, H * ss
    top = np.array([0.02, 0.07, 0.15]); bot = np.array([0.05, 0.22, 0.32])
    g = np.linspace(0, 1, Hs)[:, None, None]
    img = (top * (1 - g) + bot * g) * np.ones((Hs, Ws, 3))
    zbuf = np.full((Hs, Ws), -1e9)
    L1 = np.array([-0.45, 0.75, 0.55]); L1 /= np.linalg.norm(L1)
    L2 = np.array([0.6, -0.2, 0.5]); L2 /= np.linalg.norm(L2)
    s = px_per_unit * ss
    cen = np.asarray(center, dtype=np.float64)

    def raster(tris, color, emissive, alpha, depth_write):
        nonlocal img
        for t in tris:
            p = (t - cen) @ R.T
            n = np.cross(p[1] - p[0], p[2] - p[0])
            ln = np.linalg.norm(n)
            if ln < 1e-12:
                continue
            n /= ln
            if n[2] < 0:
                n = -n
            if emissive is not None:
                col = np.clip(np.array(color) * 0.6 + np.array(emissive) * 0.9, 0, 1)
            else:
                diff = max(0.0, float(n @ L1)); fill = max(0.0, float(n @ L2))
                col = np.clip(np.array(color) * (0.30 + 0.80 * diff) + np.array([0.04, 0.10, 0.16]) * fill, 0, 1)
            X = p[:, 0] * s + Ws / 2.0
            Y = Hs / 2.0 - p[:, 1] * s
            x0, x1 = int(max(0, math.floor(X.min()))), int(min(Ws - 1, math.ceil(X.max())))
            y0, y1 = int(max(0, math.floor(Y.min()))), int(min(Hs - 1, math.ceil(Y.max())))
            if x1 < x0 or y1 < y0:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            den = (Y[1] - Y[2]) * (X[0] - X[2]) + (X[2] - X[1]) * (Y[0] - Y[2])
            if abs(den) < 1e-9:
                continue
            w0 = ((Y[1] - Y[2]) * (xs - X[2]) + (X[2] - X[1]) * (ys - Y[2])) / den
            w1 = ((Y[2] - Y[0]) * (xs - X[2]) + (X[0] - X[2]) * (ys - Y[2])) / den
            w2 = 1 - w0 - w1
            m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            if not m.any():
                continue
            z = w0 * p[0, 2] + w1 * p[1, 2] + w2 * p[2, 2]
            sub = zbuf[y0:y1 + 1, x0:x1 + 1]
            ok = m & (z > sub)
            if not ok.any():
                continue
            region = img[y0:y1 + 1, x0:x1 + 1]
            region[ok] = region[ok] * (1 - alpha) + col * alpha
            if depth_write:
                sub[ok] = z[ok]

    order = sorted(model.parts, key=lambda k: model.materials[k]["color"][3] < 0.999)
    for key in order:
        m = model.materials[key]
        tris = model.mesh(key)
        if not len(tris):
            continue
        raster(tris, m["color"][:3], m["emissive"], m["color"][3], m["color"][3] >= 0.999)
    out = (img.reshape(H, ss, W, ss, 3).mean(axis=(1, 3)) * 255).astype(np.uint8)
    return out


def render_sheet(model, path, title, views, panel=(640, 400), px_per_unit=44, cols=2, center=(0, 0, 0)):
    from PIL import Image, ImageDraw
    W, H = panel
    rows = (len(views) + cols - 1) // cols
    sheet = Image.new("RGB", (W * cols, H * rows), (6, 14, 26))
    for i, (label, yaw, pitch) in enumerate(views):
        arr = render_view(model, yaw, pitch, W, H, px_per_unit, center=center)
        im = Image.fromarray(arr)
        d = ImageDraw.Draw(im)
        d.text((12, 10), label, fill=(190, 225, 240))
        sheet.paste(im, ((i % cols) * W, (i // cols) * H))
    d = ImageDraw.Draw(sheet)
    d.text((12, sheet.height - 18), title, fill=(150, 190, 210))
    sheet.save(path)


def write_manifest(model, out_dir, meta, files=("model.glb", "model.obj", "model.mtl", "preview.png")):
    """Validate the exported .glb by re-reading it, then write manifest.json with measured numbers only."""
    import hashlib, os
    glb = read_glb_stats(os.path.join(out_dir, "model.glb"))
    assert glb["all_finite"] and glb["triangles"] == model.stats()["triangles"], "GLB re-read mismatch"
    fl = []
    for f in files:
        pth = os.path.join(out_dir, f)
        if os.path.exists(pth):
            fl.append(dict(path=f, bytes=os.path.getsize(pth), sha256=hashlib.sha256(open(pth, "rb").read()).hexdigest()))
    mf = dict(
        id=meta["id"], title=meta["title"], status="UPLOADED_TO_GITHUB",
        generator="Procedural geometry written in Python (Assets/ModelFactory/Tools/dlmesh.py + " + meta["source_script"] + ") run in a Claude session. Not AI text-to-3D, not hand-sculpted in Blender.",
        brief=meta["brief"], reference=meta.get("reference"), files=fl,
        format="glTF 2.0 binary (.glb) plus Wavefront OBJ/MTL", textures="none - flat material colours only",
        units="metres in file (1 unit = 1 m in the design sheet); Roblox stud mapping to be set at import", axes="Y up, nose/front toward -Z, +X right (not verified against Roblox import)",
        pivot=meta["pivot"],
        measured=dict(model_stats=model.stats(), glb_reread=glb),
        materials={k: dict(color=v["color"], emissive=v["emissive"], metallic=v["metallic"], roughness=v["roughness"]) for k, v in model.materials.items()},
        license="Original procedural work created for the Deep Lantern project; no third-party assets used.",
        preview="preview.png is a software (numpy) render of the exported geometry; flat shading, not an engine render.",
        roblox_import="NOT TESTED. Suggested: import .glb/.obj via Studio 3D Importer, one MeshPart per material, set Anchored/CanCollide/CollisionFidelity in Studio; collision should use a simplified hull.",
        not_verified=["Roblox Studio import", "UV mapping (none authored; no textures)", "fit against the existing live submarine/controller contracts"],
    )
    json.dump(mf, open(os.path.join(out_dir, "manifest.json"), "w"), indent=2)
    return mf
