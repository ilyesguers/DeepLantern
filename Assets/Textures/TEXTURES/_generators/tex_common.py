"""Shared helpers for the Deep Lantern procedural texture generators.

All noise is built with wrap-around filters so every material tiles seamlessly.
"""
import os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.spatial import cKDTree

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Palette read off the Deep Lantern visual style guide (hex values approximate).
PAL = {
    "deep": "#081E3B",
    "navy": "#0B2447",
    "aqua": "#00D1FF",
    "teal": "#00A893",
    "purple": "#8B5CF6",
    "amber": "#F59E0B",
    "white": "#E6F1FF",
    "red": "#EF4444",
    "green": "#4ADE80",
    "gold": "#FBBF24",
    "blue": "#2F80ED",
    "pink": "#F472B6",
    "gray": "#94A3B8",
    "dark": "#050E1F",
}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb01(h):
    return np.array(hex2rgb(PAL.get(h, h)), dtype=np.float64) / 255.0


def rng(seed):
    return np.random.default_rng(seed)


def norm01(a):
    lo, hi = np.percentile(a, [1, 99])
    return np.clip((a - lo) / max(hi - lo, 1e-9), 0, 1)


def noise(S, sigma, seed):
    n = rng(seed).standard_normal((S, S))
    return norm01(gaussian_filter(n, sigma, mode="wrap"))


def stretched(S, sx, sy, seed):
    n = rng(seed).standard_normal((S, S))
    return norm01(gaussian_filter(n, (sy, sx), mode="wrap"))


def fbm(S, seed, base=32.0, octaves=5, gain=0.55):
    tot = np.zeros((S, S))
    for i in range(octaves):
        n = rng(seed * 101 + i).standard_normal((S, S))
        n = gaussian_filter(n, max(base / (2 ** i), 0.6), mode="wrap")
        n = (n - n.mean()) / (n.std() + 1e-9)
        tot += n * (gain ** i)
    return norm01(tot)


def ridged(n):
    return 1.0 - np.abs(2.0 * n - 1.0)


def worley(S, npts, seed):
    """Tileable Worley noise. Returns F1, F2 (pixels) and cell id per pixel."""
    r = rng(seed)
    pts = r.random((npts, 2)) * S
    tiled = np.concatenate([pts + np.array([dx * S, dy * S])
                            for dx in (-1, 0, 1) for dy in (-1, 0, 1)])
    tree = cKDTree(tiled)
    yy, xx = np.mgrid[0:S, 0:S]
    q = np.stack([xx.ravel() + 0.5, yy.ravel() + 0.5], -1)
    d, idx = tree.query(q, k=2)
    return (d[:, 0].reshape(S, S), d[:, 1].reshape(S, S),
            (idx[:, 0] % npts).reshape(S, S))


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def ramp(t, stops):
    pos = [p for p, _ in stops]
    cols = np.array([rgb01(c) for _, c in stops])
    return np.stack([np.interp(t, pos, cols[:, k]) for k in range(3)], -1)


def normal_from_height(h, strength=4.0):
    """Tileable OpenGL-style (+Y up) tangent-space normal map."""
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5
    nx, ny, nz = -gx * strength * 8, gy * strength * 8, np.ones_like(h)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    return np.stack([nx / ln, ny / ln, nz / ln], -1) * 0.5 + 0.5


def to_img(arr):
    a = (np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8)
    return Image.fromarray(a)


def save(path, arr):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    to_img(arr).save(path, optimize=True, compress_level=9)


def save_img(path, img):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=True, compress_level=9)


def seam_error(arr):
    """Ratio of wrap-edge difference to typical neighbour difference (~1 = seamless)."""
    a = arr if arr.ndim == 2 else arr.mean(-1)
    edge = (np.abs(a[:, 0] - a[:, -1]).mean() + np.abs(a[0, :] - a[-1, :]).mean()) / 2
    inner = (np.abs(a[:, 1:] - a[:, :-1]).mean() + np.abs(a[1:, :] - a[:-1, :]).mean()) / 2
    return float(edge / max(inner, 1e-9))
