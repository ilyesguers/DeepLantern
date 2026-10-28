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


def _quad_out(a, b, c, d, normal):
    """Two triangles for quad abcd, wound so the normal points along `normal`."""
    t1 = [a, b, c]; t2 = [a, c, d]
    n = np.cross(np.subtract(t1[1], t1[0]), np.subtract(t1[2], t1[0]))
    if np.dot(n, normal) < 0:
        t1 = [a, c, b]; t2 = [a, d, c]
    return [t1, t2]


def annulus(r_out, r_in, length, n=16, axis="z", pos=(0, 0, 0)):
    """Hollow ring (washer) centred on pos, extruded `length` along axis."""
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    h = length / 2.0
    tris = []
    for k in range(n):
        k2 = (k + 1) % n
        c0, s0, c1, s1 = math.cos(ang[k]), math.sin(ang[k]), math.cos(ang[k2]), math.sin(ang[k2])
        P = lambda r, c, s, z: np.array([r * c, r * s, z])
        o0b, o1b, o0t, o1t = P(r_out, c0, s0, -h), P(r_out, c1, s1, -h), P(r_out, c0, s0, h), P(r_out, c1, s1, h)
        i0b, i1b, i0t, i1t = P(r_in, c0, s0, -h), P(r_in, c1, s1, -h), P(r_in, c0, s0, h), P(r_in, c1, s1, h)
        mid = np.array([math.cos((ang[k] + (ang[k] + 2 * math.pi / n)) / 2), math.sin((ang[k] + (ang[k] + 2 * math.pi / n)) / 2), 0])
        tris += _quad_out(o0b, o1b, o1t, o0t, mid)
        tris += _quad_out(i0b, i1b, i1t, i0t, -mid)
        tris += _quad_out(o0t, o1t, i1t, i0t, np.array([0, 0, 1.0]))
        tris += _quad_out(o0b, o1b, i1b, i0b, np.array([0, 0, -1.0]))
    t = np.array(tris)
    if axis == "x":
        t = transform(t, rot=(0, 90, 0))
    elif axis == "y":
        t = transform(t, rot=(-90, 0, 0))
    return transform(t, pos=pos)


def _tri_out(a, b, c, normal):
    n = np.cross(np.subtract(b, a), np.subtract(c, a))
    return [a, b, c] if np.dot(n, normal) >= 0 else [a, c, b]


def sweep(pts, ra, rb=None, n=6, hint=(0, 0, 1), cap_start=True, cap_end=True, phase=0.0):
    """Tube along a 3D polyline. ra/rb: scalar or per-point radii (width along `side`, thickness along normal).
    Use ra>>rb for ribbon-like fronds. hint picks the side direction (cross(tangent, hint))."""
    pts = np.asarray(pts, dtype=np.float64)
    m = len(pts)
    ra = np.broadcast_to(np.asarray(ra, dtype=np.float64), (m,))
    rb = ra if rb is None else np.broadcast_to(np.asarray(rb, dtype=np.float64), (m,))
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False) + phase
    rings = []
    for i in range(m):
        t = pts[min(i + 1, m - 1)] - pts[max(i - 1, 0)]
        t = t / np.linalg.norm(t)
        side = np.cross(t, hint)
        if np.linalg.norm(side) < 1e-6:
            side = np.cross(t, (1, 0, 0))
        side /= np.linalg.norm(side)
        nrm = np.cross(t, side)
        rings.append(pts[i] + np.outer(np.cos(ang) * ra[i], side) + np.outer(np.sin(ang) * rb[i], nrm))
    tris = []
    for i in range(m - 1):
        cen = (rings[i].mean(axis=0) + rings[i + 1].mean(axis=0)) / 2
        for k in range(n):
            k2 = (k + 1) % n
            a, b, c, d = rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]
            tris += _quad_out(a, b, c, d, (a + b + c + d) / 4 - cen)
    if cap_start:
        ctr = rings[0].mean(axis=0)
        for k in range(n):
            tris.append(_tri_out(ctr, rings[0][k], rings[0][(k + 1) % n], pts[0] - pts[1]))
    if cap_end:
        ctr = rings[-1].mean(axis=0)
        for k in range(n):
            tris.append(_tri_out(ctr, rings[-1][k], rings[-1][(k + 1) % n], pts[-1] - pts[-2]))
    return np.array(tris)


def rough_loft(sections, n=9, seed=0, rough=0.2, power=2.0):
    """Like loft() but each vertex radius is jittered with a seeded RNG (deterministic organic shapes)."""
    rng = np.random.default_rng(seed)
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    c, s = np.cos(ang), np.sin(ang)
    ex = 2.0 / power
    px, py = np.sign(c) * np.abs(c) ** ex, np.sign(s) * np.abs(s) ** ex
    base = 1 + rough * (rng.random(n) * 2 - 1)
    rings = []
    for sec in sections:
        z, rx, ry = sec[0], sec[1], sec[2]
        cx = sec[3] if len(sec) > 3 else 0.0
        cy = sec[4] if len(sec) > 4 else 0.0
        j = base * (1 + 0.5 * rough * (rng.random(n) * 2 - 1))
        rings.append(np.stack([cx + px * rx * j, cy + py * ry * j, np.full(n, z)], axis=1))
    tris = []
    for i in range(len(rings) - 1):
        a, b = rings[i], rings[i + 1]
        for k in range(n):
            k2 = (k + 1) % n
            tris += [[a[k], a[k2], b[k2]], [a[k], b[k2], b[k]]]
    for ring, flip in ((rings[0], True), (rings[-1], False)):
        ctr = ring.mean(axis=0)
        for k in range(n):
            tris.append([ctr, ring[(k + 1) % n], ring[k]] if flip else [ctr, ring[k], ring[(k + 1) % n]])
    return _orient_outward(tris)


def blob(rx, ry, rz, seed=0, rough=0.18, lat=5, lon=9, pos=(0, 0, 0), rot=(0, 0, 0)):
    """Rounded lumpy ellipsoid (ry = vertical half-height), centred on pos."""
    secs = []
    for j in range(lat + 1):
        th = math.pi * j / lat
        r = max(math.sin(th), 0.08)
        secs.append((-ry * math.cos(th), rx * r, rz * r))
    t = transform(rough_loft(secs, n=lon, seed=seed, rough=rough), rot=(-90, 0, 0))
    return transform(t, rot=rot, pos=pos)


def arc_points(center, radius_x, radius_y, a0, a1, count, plane="xy"):
    pts = []
    for i in range(count):
        a = math.radians(a0 + (a1 - a0) * i / (count - 1))
        x, y = center[0] + math.cos(a) * radius_x, center[1] + math.sin(a) * radius_y
        pts.append((x, y, center[2]) if plane == "xy" else (x, center[1], y))
    return pts


def combine(name, placements):
    """Merge models into a new Model. placements: [(Model, (x,y,z) offset[, (rx,ry,rz)])]."""
    out = Model(name)
    for pl in placements:
        mdl, off = pl[0], pl[1]
        rot = pl[2] if len(pl) > 2 else (0, 0, 0)
        for key, mat in mdl.materials.items():
            if key not in out.materials:
                out.materials[key] = dict(mat); out.parts.setdefault(key, [])
            tris = mdl.mesh(key)
            if len(tris):
                out.parts[key].append(transform(tris, rot=rot, pos=off))
    return out


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
            if not len(self.parts.get(key, [])):
                continue
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


def write_manifest(model, out_dir, meta, files=("model.glb", "model.obj", "model.mtl", "preview.png"), extra=None):
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
        generator="Procedural geometry written in Python (Assets/ModelFactory/Tools/dlmesh.py v2 + " + meta["source_script"] + ") run in a Claude session. Not AI text-to-3D, not hand-sculpted in Blender. v2 adds chamfered edges, baked vertex-colour ambient occlusion, smoothed normals, box-projected UVs and procedural grayscale detail textures.",
        brief=meta["brief"], reference=meta.get("reference"), files=fl,
        format="glTF 2.0 binary (.glb; textures embedded) plus Wavefront OBJ/MTL (with vn/vt and AO vertex colours)", textures="procedural grayscale detail maps (256 px, tileable, multiplied with the material colour): panel, metal, rock, organic - see textures/; emissive, glass and FX materials are untextured",
        units="metres in file (1 unit = 1 m in the design sheet); Roblox stud mapping to be set at import", axes="Y up, nose/front toward -Z, +X right (not verified against Roblox import)",
        pivot=meta["pivot"],
        measured=dict(model_stats=model.stats(), glb_reread=glb),
        materials={k: dict(color=v["color"], emissive=v["emissive"], metallic=v["metallic"], roughness=v["roughness"]) for k, v in model.materials.items() if len(model.parts.get(k, []))},
        license="Original procedural work created for the Deep Lantern project; no third-party assets used.",
        preview="preview.png is a software (numpy) render of the exported geometry; flat shading, not an engine render.",
        roblox_import="NOT TESTED. Suggested: import .glb/.obj via Studio 3D Importer, one MeshPart per material, set Anchored/CanCollide/CollisionFidelity in Studio; collision should use a simplified hull.",
        not_verified=["Roblox Studio import", "UV quality (simple box projection; seams and stretching possible on curved parts)", "fit against the existing live submarine/controller contracts"],
    )
    if extra:
        mf.update(extra)
    json.dump(mf, open(os.path.join(out_dir, "manifest.json"), "w"), indent=2)
    return mf


def emit(out_dir, meta, collection, parts=None, views=None, px=44, center=(0, 0, 0), title="", panel=(640, 400), cols=2):
    """Write collection (model.glb/.obj/.mtl), optional per-part .glb files under parts/, preview and manifest."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    collection.write_glb(os.path.join(out_dir, "model.glb"))
    collection.write_obj(os.path.join(out_dir, "model.obj"), "model.mtl")
    collection.write_mtl(os.path.join(out_dir, "model.mtl"))
    tex_files = collection.write_textures(os.path.join(out_dir, "textures"))
    files = ["model.glb", "model.obj", "model.mtl", "preview.png"] + tex_files
    extra = {}
    if parts:
        os.makedirs(os.path.join(out_dir, "parts"), exist_ok=True)
        pinfo = {}
        for pname, pm in parts.items():
            rel = f"parts/{pname}.glb"
            pm.write_glb(os.path.join(out_dir, rel))
            st = read_glb_stats(os.path.join(out_dir, rel))
            assert st["all_finite"] and st["triangles"] == pm.stats()["triangles"]
            pinfo[pname] = dict(file=rel, triangles=st["triangles"], size=pm.stats()["size"],
                                bounds_min=st["bounds_min"], bounds_max=st["bounds_max"])
            files.append(rel)
        extra["parts"] = pinfo
    render_sheet(collection, os.path.join(out_dir, "preview.png"), title, views, panel=panel, px_per_unit=px, cols=cols, center=center)
    write_manifest(collection, out_dir, meta, files=tuple(files), extra=extra)
    return collection.stats()


def std_materials(m, extra=()):
    """Shared Deep Lantern palette (navy/graphite, off-white, amber, cyan, selective glow)."""
    m.material("hull_offwhite", (0.84, 0.87, 0.90), metallic=0.15, roughness=0.55)
    m.material("graphite_navy", (0.07, 0.10, 0.17), metallic=0.45, roughness=0.55)
    m.material("amber_accent", (0.93, 0.58, 0.10), metallic=0.2, roughness=0.5)
    m.material("glass_cyan", (0.30, 0.78, 0.95), metallic=0.0, roughness=0.1, alpha=0.5)
    m.material("emissive_cyan", (0.10, 0.55, 0.80), emissive=(0.25, 0.85, 1.0), roughness=0.4)
    for e in extra:
        if e == "teal_shell":
            m.material("teal_shell", (0.07, 0.27, 0.32), metallic=0.3, roughness=0.6)
        elif e == "titanium":
            m.material("titanium", (0.62, 0.66, 0.70), metallic=0.85, roughness=0.35)
        elif e == "specimen_violet":
            m.material("specimen_violet", (0.45, 0.25, 0.75), emissive=(0.55, 0.30, 0.95), roughness=0.4)
        elif e in ("coral_pink", "coral_orange", "coral_violet", "coral_mint", "coral_turq", "shadow_blue"):
            col = dict(coral_pink=(0.90, 0.42, 0.55), coral_orange=(0.95, 0.52, 0.22), coral_violet=(0.50, 0.32, 0.72),
                       coral_mint=(0.55, 0.88, 0.72), coral_turq=(0.15, 0.72, 0.75), shadow_blue=(0.06, 0.14, 0.28))[e]
            m.material(e, col, metallic=0.0, roughness=0.8)
        elif e in ("kelp_deep", "kelp_mid", "kelp_lime", "kelp_gold"):
            col = dict(kelp_deep=(0.04, 0.26, 0.24), kelp_mid=(0.20, 0.52, 0.38), kelp_lime=(0.52, 0.74, 0.24), kelp_gold=(0.78, 0.62, 0.20))[e]
            m.material(e, col, metallic=0.0, roughness=0.75)
        elif e in ("stone_blue", "stone_warm", "sediment"):
            col = dict(stone_blue=(0.30, 0.38, 0.47), stone_warm=(0.52, 0.43, 0.37), sediment=(0.62, 0.58, 0.48))[e]
            m.material(e, col, metallic=0.0, roughness=0.9)
        elif e in ("flora_body", "flora_violet"):
            m.material(e, (0.08, 0.22, 0.30) if e == "flora_body" else (0.26, 0.18, 0.42), metallic=0.0, roughness=0.7)
        elif e == "emissive_teal":
            m.material(e, (0.10, 0.50, 0.50), emissive=(0.20, 0.95, 0.85), roughness=0.4)
        elif e == "emissive_violet":
            m.material(e, (0.35, 0.20, 0.55), emissive=(0.65, 0.35, 1.0), roughness=0.4)
        elif e in ("metal_dark", "faded_blue", "corrosion", "mineral"):
            col = dict(metal_dark=(0.13, 0.15, 0.19), faded_blue=(0.18, 0.34, 0.50), corrosion=(0.36, 0.23, 0.13), mineral=(0.62, 0.68, 0.64))[e]
            m.material(e, col, metallic=0.5 if e == "metal_dark" else 0.1, roughness=0.7)
        elif e == "relic_stone":
            m.material(e, (0.22, 0.25, 0.30), metallic=0.1, roughness=0.85)
        elif e == "emissive_amber":
            m.material("emissive_amber", (0.80, 0.50, 0.10), emissive=(1.0, 0.72, 0.25), roughness=0.4)


# =============================================================================
# v2 quality pass (overrides earlier definitions of box / write_glb / write_obj /
# write_mtl / render_view / std_materials). Adds: chamfered boxes, voxel-baked
# ambient occlusion in vertex colours, angle-smoothed normals, box-projected UVs
# with procedural tiling detail textures (embedded in the .glb), static light-beam
# FX meshes, and a preview renderer with specular light, fog and bloom.
# =============================================================================
import io as _io
import itertools as _it

AUTO_BEVEL = True
_box_plain = box


def _hull_faces(P, eps=1e-6):
    P = np.asarray(P, dtype=np.float64)
    n = len(P)
    planes = {}
    for i, j, k in _it.combinations(range(n), 3):
        nr = np.cross(P[j] - P[i], P[k] - P[i])
        ln = np.linalg.norm(nr)
        if ln < eps:
            continue
        nr = nr / ln
        d = float(nr @ P[i])
        side = P @ nr - d
        if (side <= eps).all():
            pass
        elif (side >= -eps).all():
            nr, d = -nr, -d
        else:
            continue
        key = tuple(np.round(np.append(nr, d), 4))
        planes[key] = (nr, d)
    faces = []
    for nr, d in planes.values():
        idx = np.where(np.abs(P @ nr - d) < 1e-5)[0]
        c = P[idx].mean(axis=0)
        a = np.cross(nr, [1, 0, 0]) if abs(nr[0]) < 0.9 else np.cross(nr, [0, 1, 0])
        a /= np.linalg.norm(a)
        b = np.cross(nr, a)
        ang = np.arctan2((P[idx] - c) @ b, (P[idx] - c) @ a)
        faces.append([int(x) for x in idx[np.argsort(ang)]])
    return faces


def hull_tris(points):
    """Triangles of the convex hull of a point set (outward-wound)."""
    P = np.asarray(points, dtype=np.float64)
    tris = []
    for f in _hull_faces(P):
        for k in range(1, len(f) - 1):
            tris.append([P[f[0]], P[f[k]], P[f[k + 1]]])
    return _orient_outward(tris)


_CHAMFER_TOPO = {}


def _chamfer_points(a, b, d, c):
    pts = []
    for sx, sy, sz in _it.product((-1, 1), repeat=3):
        pts.append((sx * a, sy * (b - c), sz * (d - c)))
        pts.append((sx * (a - c), sy * b, sz * (d - c)))
        pts.append((sx * (a - c), sy * (b - c), sz * d))
    return np.array(pts, dtype=np.float64)


def box(size, pos=(0, 0, 0), rot=(0, 0, 0), bevel=None):  # noqa: F811
    """Axis-aligned box; v2 chamfers the edges so they catch light (bevel in metres)."""
    mn = min(size)
    if bevel is None:
        bevel = min(0.03, 0.22 * mn) if AUTO_BEVEL else 0.0
    if bevel < 0.003 or mn < 0.03:
        return _box_plain(size, pos, rot)
    c = min(bevel, 0.4 * mn)
    a, b, d = (s / 2.0 for s in size)
    if "faces" not in _CHAMFER_TOPO:
        ref = _chamfer_points(1.0, 1.0, 1.0, 0.25)
        _CHAMFER_TOPO["faces"] = _hull_faces(ref)
    P = _chamfer_points(a, b, d, c)
    tris = []
    for f in _CHAMFER_TOPO["faces"]:
        for k in range(1, len(f) - 1):
            tris.append([P[f[0]], P[f[k]], P[f[k + 1]]])
    return transform(np.array(tris), rot, pos)


def orient_z_to(tris, direction, pos=(0, 0, 0)):
    """Rotate geometry built along +Z so +Z points along `direction`, then translate."""
    d = np.asarray(direction, dtype=np.float64)
    d = d / np.linalg.norm(d)
    z = np.array([0, 0, 1.0])
    v = np.cross(z, d)
    s, c = np.linalg.norm(v), float(z @ d)
    if s < 1e-9:
        R = np.eye(3) if c > 0 else np.diag([1, -1, -1.0])
    else:
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        R = np.eye(3) + vx + vx @ vx * ((1 - c) / (s * s))
    return np.asarray(tris) @ R.T + np.asarray(pos, dtype=np.float64)


def light_beam(model, key, pos, direction, length=3.0, r0=0.15, r1=0.9, n=12):
    """Static translucent light-shaft cone (visual FX mesh, not a light, no script)."""
    cone = loft([(0.0, r0, r0), (length, r1, r1)], n=n, cap_start=False, cap_end=False)
    model.add(key, orient_z_to(cone, direction, pos))


def fx_material(model, key, color=(0.2, 0.85, 1.0), alpha=0.10):
    model.material(key, color, emissive=color, metallic=0.0, roughness=1.0, alpha=alpha)


# ---- procedural detail textures (grayscale, tileable, multiplied with base colour) ----
_TEX_CACHE = {}
TEX_RES = 256


def _pnoise(rng, power=1.5, aniso=(1.0, 1.0), res=TEX_RES):
    F = np.fft.fft2(rng.standard_normal((res, res)))
    fy = np.fft.fftfreq(res)[:, None] * aniso[0]
    fx = np.fft.fftfreq(res)[None, :] * aniso[1]
    r = np.sqrt(fx ** 2 + fy ** 2)
    r[0, 0] = 1.0
    F = F / (r ** power)
    F[0, 0] = 0
    n = np.fft.ifft2(F).real
    return (n - n.min()) / (n.max() - n.min() + 1e-9)


def _wrap_draw(draw_fn, res=TEX_RES):
    for ox in (-res, 0, res):
        for oy in (-res, 0, res):
            draw_fn(ox, oy)


def make_texture(kind, seed=1):
    from PIL import Image, ImageDraw, ImageFilter
    if (kind, seed) in _TEX_CACHE:
        return _TEX_CACHE[(kind, seed)]
    res = TEX_RES
    rng = np.random.default_rng(abs(hash(kind)) % 1000 + seed)
    if kind == "panel":
        base = 0.84 + 0.12 * _pnoise(rng, 1.6)
        im = Image.fromarray((base * 255).astype(np.uint8), "L")
        d = ImageDraw.Draw(im)
        for g in (0, res // 2):
            _wrap_draw(lambda ox, oy, g=g: (d.line([(g + ox, oy), (g + ox, res + oy)], fill=118, width=3),
                                             d.line([(ox, g + oy), (res + ox, g + oy)], fill=118, width=3),
                                             d.line([(g + 2 + ox, oy), (g + 2 + ox, res + oy)], fill=250, width=1),
                                             d.line([(ox, g + 2 + oy), (res + ox, g + 2 + oy)], fill=250, width=1)))
        for g in (0, res // 2):
            for t in range(0, res, 32):
                for (x, y) in ((g, t), (t, g)):
                    _wrap_draw(lambda ox, oy, x=x, y=y: d.ellipse([x - 3 + ox, y - 3 + oy, x + 3 + ox, y + 3 + oy], fill=95))
                    _wrap_draw(lambda ox, oy, x=x, y=y: d.ellipse([x - 1 + ox, y - 2 + oy, x + 1 + ox, y + oy], fill=255))
        for _ in range(26):
            x, y = rng.integers(0, res, 2); L = rng.integers(10, 55); a = rng.uniform(0, 6.28)
            _wrap_draw(lambda ox, oy: d.line([(x + ox, y + oy), (x + np.cos(a) * L + ox, y + np.sin(a) * L + oy)], fill=int(rng.integers(150, 215)), width=1))
        arr = np.asarray(im, dtype=np.float64) / 255.0
    elif kind == "metal":
        base = 0.80 + 0.14 * _pnoise(rng, 1.4, aniso=(1.0, 0.05))
        base += 0.04 * (_pnoise(rng, 0.8) - 0.5)
        im = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8), "L")
        d = ImageDraw.Draw(im)
        _wrap_draw(lambda ox, oy: (d.line([(res // 2 + ox, oy), (res // 2 + ox, res + oy)], fill=110, width=3),
                                    d.line([(ox, res // 2 + oy), (res + ox, res // 2 + oy)], fill=110, width=3)))
        for (x, y) in ((res // 2, 16), (res // 2, res - 16), (16, res // 2), (res - 16, res // 2)):
            _wrap_draw(lambda ox, oy, x=x, y=y: d.ellipse([x - 4 + ox, y - 4 + oy, x + 4 + ox, y + 4 + oy], fill=90))
            _wrap_draw(lambda ox, oy, x=x, y=y: d.ellipse([x - 2 + ox, y - 3 + oy, x + ox, y - 1 + oy], fill=255))
        for _ in range(34):
            x, y = rng.integers(0, res, 2); L = rng.integers(8, 70); a = rng.normal(0, 0.25)
            _wrap_draw(lambda ox, oy: d.line([(x + ox, y + oy), (x + np.cos(a) * L + ox, y + np.sin(a) * L + oy)], fill=int(rng.integers(140, 235)), width=1))
        arr = np.asarray(im, dtype=np.float64) / 255.0
    elif kind == "rock":
        n1 = _pnoise(rng, 1.3); n2 = _pnoise(rng, 2.2)
        yy = np.linspace(0, 1, res, endpoint=False)[:, None]
        strata = 0.07 * np.sin(2 * np.pi * (yy * 3 + 0.8 * n2))
        arr = 0.62 + 0.30 * n1 + strata
        im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "L")
        d = ImageDraw.Draw(im)
        for _ in range(9):
            x, y = rng.integers(0, res, 2)
            pts = [(x, y)]
            for _s in range(7):
                x += rng.integers(-18, 18); y += rng.integers(6, 26); pts.append((x, y))
            _wrap_draw(lambda ox, oy: d.line([(p[0] + ox, p[1] + oy) for p in pts], fill=70, width=1))
        arr = np.asarray(im.filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float64) / 255.0
    else:  # organic
        arr = 0.74 + 0.20 * _pnoise(rng, 1.8) + 0.05 * (_pnoise(rng, 0.7) - 0.5)
        mott = _pnoise(rng, 2.6)
        arr = arr - 0.10 * (mott > 0.72)
    img = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "L").convert("RGB")
    _TEX_CACHE[(kind, seed)] = img
    return img


def tex_kind_for(key):
    if key.startswith("fx_") or key.startswith("emissive") or key.startswith("glass") or key.startswith("specimen"):
        return None
    for pre in ("stone", "sediment", "mineral", "relic", "corrosion"):
        if key.startswith(pre):
            return "rock"
    for pre in ("coral", "kelp", "flora", "shadow_blue", "fish", "jelly"):
        if key.startswith(pre):
            return "organic"
    for pre in ("hull", "amber", "faded_blue"):
        if key.startswith(pre):
            return "panel"
    return "metal"


# ---- baking: smoothed normals, ambient occlusion, UVs --------------------------------
def _smooth_normals(tris, angle=55.0):
    N = len(tris)
    fn = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    area = np.linalg.norm(fn, axis=1)
    fu = np.where(area[:, None] > 1e-12, fn / np.maximum(area[:, None], 1e-12), np.array([0, 1.0, 0]))
    out = np.repeat(fu, 3, axis=0)
    key = np.round(tris.reshape(-1, 3) * 1e4).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    order = np.argsort(inv, kind="stable")
    sinv = inv[order]
    bounds = np.flatnonzero(np.diff(sinv)) + 1
    cosT = math.cos(math.radians(angle))
    for grp in np.split(order, bounds):
        if len(grp) < 2:
            continue
        tid = grp // 3
        nr = fu[tid] * area[tid][:, None]
        for c, t in zip(grp, tid):
            msk = (fu[tid] @ fu[t]) > cosT
            v = nr[msk].sum(axis=0)
            ln = np.linalg.norm(v)
            if ln > 1e-12:
                out[c] = v / ln
    return out


def _bake_ao(model, occl_keys, strength=0.65):
    """Per-tri-corner AO for every material by marching rays through a voxelised copy of the model."""
    allt = [model.mesh(k) for k in occl_keys if len(model.parts[k])]
    if not allt:
        return {}
    T = np.concatenate(allt, axis=0)
    v = T.reshape(-1, 3)
    lo, hi = v.min(axis=0) - 0.05, v.max(axis=0) + 0.05
    ext = float((hi - lo).max())
    vox = ext / 110.0
    dims = np.ceil((hi - lo) / vox).astype(int) + 1
    occ = np.zeros(tuple(dims), dtype=bool)
    for t in T:
        e = max(np.linalg.norm(t[1] - t[0]), np.linalg.norm(t[2] - t[1]), np.linalg.norm(t[0] - t[2]))
        n = max(1, int(math.ceil(e / (vox * 0.7))))
        ii, jj = np.meshgrid(np.arange(n + 1), np.arange(n + 1))
        m = (ii + jj) <= n
        a = (ii[m] / n)[:, None]; b = (jj[m] / n)[:, None]
        P = t[0] + a * (t[1] - t[0]) + b * (t[2] - t[0])
        idx = np.floor((P - lo) / vox).astype(int)
        occ[idx[:, 0], idx[:, 1], idx[:, 2]] = True
    rng = np.random.default_rng(7)
    dirs = rng.normal(size=(14, 3)); dirs[:, 1] = np.abs(dirs[:, 1]) * 0.0 + dirs[:, 1]
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    R = 0.12 * ext
    steps = np.array([0.18, 0.36, 0.6, 1.0]) * R
    wts = np.array([1.0, 0.8, 0.55, 0.3])
    res = {}
    for key in model.parts:
        tris = model.mesh(key)
        if not len(tris):
            continue
        fn = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        fu = fn / np.maximum(np.linalg.norm(fn, axis=1, keepdims=True), 1e-12)
        ao_t = np.ones((len(tris), 3))
        # sample per corner, nudged slightly toward the triangle centre
        cen = tris.mean(axis=1)
        for c in range(3):
            P = tris[:, c] * 0.8 + cen * 0.2
            hit = np.zeros(len(tris))
            for d in dirs:
                dd = np.broadcast_to(d, fu.shape)
                dd = np.where((fu * dd).sum(axis=1, keepdims=True) < 0, -dd, dd)
                dd = dd * 0.75 + fu * 0.35
                dd /= np.linalg.norm(dd, axis=1, keepdims=True)
                h = np.zeros(len(tris), dtype=bool)
                for s, w in zip(steps, wts):
                    q = P + fu * vox * 1.9 + dd * s
                    ix = np.floor((q - lo) / vox).astype(int)
                    ok = (ix >= 0).all(axis=1) & (ix < dims).all(axis=1)
                    got = np.zeros(len(tris), dtype=bool)
                    got[ok] = occ[ix[ok, 0], ix[ok, 1], ix[ok, 2]]
                    newly = got & ~h
                    hit[newly] += w
                    h |= got
            ao_t[:, c] = hit / (len(dirs) * wts[0])
        res[key] = np.clip(1.0 - strength * ao_t, 0.3, 1.0)
    return res, (lo, hi)


def bake(model):
    """Returns {material: dict(pos, nrm, col, uv)} with per-corner arrays (3 corners per triangle)."""
    sig = (len(model.parts), sum(len(model.mesh(k)) for k in model.parts))
    if getattr(model, "_bake_sig", None) == sig:
        return model._bake
    solid = [k for k in model.parts if len(model.parts[k]) and not k.startswith("fx_") and model.materials[k]["color"][3] > 0.6]
    ao, bnd = _bake_ao(model, solid)
    ymin, ymax = bnd[0][1], bnd[1][1]
    out = {}
    for key in model.parts:
        tris = model.mesh(key)
        if not len(tris):
            continue
        pos = tris.reshape(-1, 3)
        nrm = _smooth_normals(tris)
        if key in ao:
            aoc = ao[key].reshape(-1)
            grad = 0.86 + 0.14 * np.clip((pos[:, 1] - ymin) / max(ymax - ymin, 1e-6), 0, 1)
            col = np.repeat((aoc * grad)[:, None], 3, axis=1)
        else:
            col = np.ones((len(pos), 3))
        fn = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        ax = np.argmax(np.abs(fn), axis=1)
        tile = float(model.materials[key].get("tile", 1.0))
        uv = np.zeros((len(tris), 3, 2))
        for a in range(3):
            m = ax == a
            if not m.any():
                continue
            c = [(2, 1), (0, 2), (0, 1)][a]
            sgn = np.where(fn[m, a] < 0, -1.0, 1.0)[:, None]
            uv[m, :, 0] = tris[m][:, :, c[0]] * sgn / tile
            uv[m, :, 1] = tris[m][:, :, c[1]] / tile
        out[key] = dict(pos=pos.astype(np.float32), nrm=nrm.astype(np.float32), col=col.astype(np.float32),
                        uv=uv.reshape(-1, 2).astype(np.float32), tex=tex_kind_for(key))
    model._bake, model._bake_sig = out, sig
    return out


def _png_bytes(img):
    b = _io.BytesIO()
    img.save(b, "PNG", optimize=True)
    return b.getvalue()


def _write_glb_v2(self, path):
    B = bake(self)
    bin_chunks, views, accessors, meshes, nodes, mats, images, textures = [], [], [], [], [], [], [], []
    img_index = {}
    offset = 0

    def push(data, target=None):
        nonlocal offset
        pad = (-len(data)) % 4
        v = dict(buffer=0, byteOffset=offset, byteLength=len(data))
        if target:
            v["target"] = target
        views.append(v)
        bin_chunks.append(data + b"\0" * pad)
        offset += len(data) + pad
        return len(views) - 1

    keys = [k for k in self.parts if k in B]
    for mi, key in enumerate(keys):
        m = self.materials[key]; d = B[key]
        pos, nor, col, uv = d["pos"], d["nrm"], d["col"], d["uv"]
        idx = np.arange(len(pos), dtype=np.uint32)
        a0 = len(accessors)
        accessors.append(dict(bufferView=push(pos.tobytes(), 34962), componentType=5126, count=len(pos), type="VEC3",
                              min=[float(x) for x in pos.min(axis=0)], max=[float(x) for x in pos.max(axis=0)]))
        accessors.append(dict(bufferView=push(nor.tobytes(), 34962), componentType=5126, count=len(nor), type="VEC3"))
        accessors.append(dict(bufferView=push(idx.tobytes(), 34963), componentType=5125, count=len(idx), type="SCALAR"))
        attrs = dict(POSITION=a0, NORMAL=a0 + 1)
        accessors.append(dict(bufferView=push(col.tobytes(), 34962), componentType=5126, count=len(col), type="VEC3"))
        attrs["COLOR_0"] = len(accessors) - 1
        pbr = dict(baseColorFactor=[float(c) for c in m["color"]], metallicFactor=float(m["metallic"]), roughnessFactor=float(m["roughness"]))
        if d["tex"]:
            accessors.append(dict(bufferView=push(uv.tobytes(), 34962), componentType=5126, count=len(uv), type="VEC2"))
            attrs["TEXCOORD_0"] = len(accessors) - 1
            if d["tex"] not in img_index:
                images.append(dict(bufferView=push(_png_bytes(make_texture(d["tex"]))), mimeType="image/png", name=f"detail_{d['tex']}"))
                textures.append(dict(source=len(images) - 1, sampler=0))
                img_index[d["tex"]] = len(textures) - 1
            pbr["baseColorTexture"] = dict(index=img_index[d["tex"]])
        mat = dict(name=key, pbrMetallicRoughness=pbr, doubleSided=True)
        if m["emissive"] is not None:
            mat["emissiveFactor"] = [float(c) for c in m["emissive"]]
        if m["color"][3] < 0.999:
            mat["alphaMode"] = "BLEND"
        mats.append(mat)
        meshes.append(dict(name=f"{self.name}_{key}", primitives=[dict(attributes=attrs, indices=a0 + 2, material=mi, mode=4)]))
        nodes.append(dict(name=f"{self.name}_{key}", mesh=mi))
    gltf = dict(asset=dict(version="2.0", generator="Deep Lantern dlmesh.py v2 (procedural geometry, baked AO, detail textures; no AI)"),
                scene=0, scenes=[dict(nodes=[len(nodes)])], nodes=nodes + [dict(name=self.name, children=list(range(len(nodes))))],
                meshes=meshes, materials=mats, accessors=accessors, bufferViews=views, buffers=[dict(byteLength=offset)])
    if images:
        gltf["images"], gltf["textures"] = images, textures
        gltf["samplers"] = [dict(magFilter=9729, minFilter=9987, wrapS=10497, wrapT=10497)]
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * ((-len(js)) % 4)
    binb = b"".join(bin_chunks)
    total = 12 + 8 + len(js) + 8 + len(binb)
    with open(path, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, total))
        f.write(struct.pack("<I4s", len(js), b"JSON") + js)
        f.write(struct.pack("<I4s", len(binb), b"BIN\0") + binb)


def _write_obj_v2(self, obj_path, mtl_name):
    B = bake(self)
    lines = [f"# {self.name} - Deep Lantern dlmesh.py v2 (procedural geometry; v lines carry baked AO colour)", f"mtllib {mtl_name}"]
    vb = 1
    for key in self.parts:
        if key not in B:
            continue
        d = B[key]
        lines += [f"o {self.name}_{key}", f"usemtl {key}", "s 1"]
        for p, c in zip(d["pos"], d["col"]):
            lines.append("v %.5f %.5f %.5f %.3f %.3f %.3f" % (*p, *c))
        for n in d["nrm"]:
            lines.append("vn %.4f %.4f %.4f" % tuple(n))
        for t in d["uv"]:
            lines.append("vt %.5f %.5f" % tuple(t))
        for i in range(len(d["pos"]) // 3):
            b = vb + i * 3
            if d["tex"]:
                lines.append(f"f {b}/{b}/{b} {b+1}/{b+1}/{b+1} {b+2}/{b+2}/{b+2}")
            else:
                lines.append(f"f {b}//{b} {b+1}//{b+1} {b+2}//{b+2}")
        vb += len(d["pos"])
    open(obj_path, "w").write("\n".join(lines) + "\n")


def _write_mtl_v2(self, mtl_path):
    B = bake(self)
    out = []
    for key, m in self.materials.items():
        if key not in B:
            continue
        c = m["color"]
        out += [f"newmtl {key}", "Kd %.4f %.4f %.4f" % c[:3], "d %.3f" % c[3]]
        if m["emissive"] is not None:
            out.append("Ke %.4f %.4f %.4f" % tuple(m["emissive"]))
        if B[key]["tex"]:
            out.append(f"map_Kd textures/detail_{B[key]['tex']}.png")
        out.append("")
    open(mtl_path, "w").write("\n".join(out))


def _write_textures(self, tex_dir):
    import os
    os.makedirs(tex_dir, exist_ok=True)
    kinds = sorted({d["tex"] for d in bake(self).values() if d["tex"]})
    for k in kinds:
        make_texture(k).save(os.path.join(tex_dir, f"detail_{k}.png"), optimize=True)
    return [f"textures/detail_{k}.png" for k in kinds]


Model.write_glb = _write_glb_v2
Model.write_obj = _write_obj_v2
Model.write_mtl = _write_mtl_v2
Model.write_textures = _write_textures

_std_materials_v1 = std_materials


def std_materials(m, extra=()):  # noqa: F811
    _std_materials_v1(m, extra)
    fx_material(m, "fx_beam_cyan", (0.25, 0.85, 1.0), 0.10)
    fx_material(m, "fx_beam_amber", (1.0, 0.75, 0.30), 0.10)
    fx_material(m, "fx_halo_teal", (0.20, 0.95, 0.85), 0.16)
    fx_material(m, "fx_halo_violet", (0.65, 0.35, 1.0), 0.16)


# ---- preview renderer v2 ------------------------------------------------------------
def _box_blur(a, r, passes=3):
    for _ in range(passes):
        for ax in (0, 1):
            c = np.cumsum(np.pad(a, [(r + 1, r) if i == ax else (0, 0) for i in range(a.ndim)], mode="edge"), axis=ax)
            n = a.shape[ax]
            sl = lambda s, e: tuple(slice(s, e) if i == ax else slice(None) for i in range(a.ndim))
            a = (c[sl(2 * r + 1, 2 * r + 1 + n)] - c[sl(0, n)]) / (2 * r + 1)
    return a


def render_view(model, yaw, pitch, W, H, px_per_unit, ss=2, center=(0, 0, 0)):  # noqa: F811
    B = bake(model)
    R = _view_matrix(yaw, pitch)
    Ws, Hs = W * ss, H * ss
    top = np.array([0.015, 0.05, 0.12]); bot = np.array([0.05, 0.24, 0.34])
    g = np.linspace(0, 1, Hs)[:, None, None]
    img = (top * (1 - g) + bot * g) * np.ones((Hs, Ws, 3))
    zbuf = np.full((Hs, Ws), -1e9)
    glow = np.zeros((Hs, Ws, 3))
    Lk = np.array([-0.45, 0.80, 0.55]); Lk /= np.linalg.norm(Lk)
    Lf = np.array([0.65, -0.15, 0.45]); Lf /= np.linalg.norm(Lf)
    camdir = R.T @ np.array([0, 0, 1.0])
    s = px_per_unit * ss
    cen = np.asarray(center, dtype=np.float64)
    texarr = {}

    def sample(kind, uv):
        if kind not in texarr:
            texarr[kind] = np.asarray(make_texture(kind), dtype=np.float64)[..., :1] / 255.0
        t = texarr[kind]
        ix = (np.floor(uv[..., 0] * t.shape[1]).astype(int)) % t.shape[1]
        iy = (np.floor(uv[..., 1] * t.shape[0]).astype(int)) % t.shape[0]
        return t[iy, ix]

    def draw(key, d, alpha_pass):
        m = model.materials[key]
        base = np.array(m["color"][:3]); alpha = m["color"][3]
        emis = np.array(m["emissive"]) if m["emissive"] is not None else None
        rough = m["roughness"]; metal = m["metallic"]
        P, Nn, Cc, UV = d["pos"], d["nrm"], d["col"], d["uv"]
        pc = (P - cen) @ R.T
        for i in range(len(P) // 3):
            sl = slice(i * 3, i * 3 + 3)
            p = pc[sl]
            X = p[:, 0] * s + Ws / 2.0; Y = Hs / 2.0 - p[:, 1] * s
            x0, x1 = int(max(0, math.floor(X.min()))), int(min(Ws - 1, math.ceil(X.max())))
            y0, y1 = int(max(0, math.floor(Y.min()))), int(min(Hs - 1, math.ceil(Y.max())))
            if x1 < x0 or y1 < y0:
                continue
            den = (Y[1] - Y[2]) * (X[0] - X[2]) + (X[2] - X[1]) * (Y[0] - Y[2])
            if abs(den) < 1e-9:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            w0 = ((Y[1] - Y[2]) * (xs - X[2]) + (X[2] - X[1]) * (ys - Y[2])) / den
            w1 = ((Y[2] - Y[0]) * (xs - X[2]) + (X[0] - X[2]) * (ys - Y[2])) / den
            w2 = 1 - w0 - w1
            mk = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            if not mk.any():
                continue
            z = w0 * p[0, 2] + w1 * p[1, 2] + w2 * p[2, 2]
            sub = zbuf[y0:y1 + 1, x0:x1 + 1]
            ok = mk & (z > sub)
            if not ok.any():
                continue
            W0, W1, W2 = w0[ok][:, None], w1[ok][:, None], w2[ok][:, None]
            n = W0 * Nn[sl][0] + W1 * Nn[sl][1] + W2 * Nn[sl][2]
            n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
            flip = (n @ camdir) < 0
            n[flip] *= -1
            ao = W0 * Cc[sl][0] + W1 * Cc[sl][1] + W2 * Cc[sl][2]
            alb = np.broadcast_to(base, ao.shape) * ao
            if d["tex"]:
                uv = W0 * UV[sl][0] + W1 * UV[sl][1] + W2 * UV[sl][2]
                alb = alb * sample(d["tex"], uv)
            diff = np.clip(n @ Lk, 0, 1)[:, None]; fill = np.clip(n @ Lf, 0, 1)[:, None]
            hemi = 0.5 + 0.5 * n[:, 1:2]
            col = alb * (0.22 + 0.22 * hemi + 0.85 * diff) + np.array([0.04, 0.12, 0.2]) * fill * alb.mean(axis=1, keepdims=True) * 2
            Hh = Lk + camdir; Hh /= np.linalg.norm(Hh)
            sp = np.clip(n @ Hh, 0, 1)[:, None] ** (6 + (1 - rough) * 70)
            col = col + sp * (0.10 + 0.55 * metal) * (1 - rough * 0.6) * (alb * metal + (1 - metal))
            rim = (1 - np.clip(n @ camdir, 0, 1))[:, None] ** 3
            col = col + rim * np.array([0.05, 0.16, 0.24]) * 0.7
            if emis is not None:
                e = np.broadcast_to(emis, col.shape)
                col = np.clip(col * 0.4 + e * 0.95, 0, 1.4)
                gy, gx = np.nonzero(ok)
                glow[y0 + gy, x0 + gx] += e * (0.9 if not alpha_pass else 0.9 * alpha)
            depth = np.clip((z[ok][:, None] - z.min()) / 12.0, 0, 1)
            col = col * (1 - 0.18 * (1 - depth)) + np.array([0.02, 0.10, 0.16]) * 0.0
            region = img[y0:y1 + 1, x0:x1 + 1]
            a = alpha if alpha < 0.999 else 1.0
            region[ok] = region[ok] * (1 - a) + np.clip(col, 0, 1) * a
            if not alpha_pass:
                sub[ok] = z[ok]

    solid = [k for k in model.parts if k in B and model.materials[k]["color"][3] >= 0.999]
    trans = [k for k in model.parts if k in B and model.materials[k]["color"][3] < 0.999]
    for k in solid:
        draw(k, B[k], False)
    for k in trans:
        draw(k, B[k], True)
    gl = _box_blur(glow, 3 * ss, 2) * 1.6 + _box_blur(glow, 10 * ss, 2) * 2.4
    img = np.clip(img + gl * 0.55, 0, 1)
    img = img ** (1 / 1.08)
    return (img.reshape(H, ss, W, ss, 3).mean(axis=(1, 3)) * 255).astype(np.uint8)
