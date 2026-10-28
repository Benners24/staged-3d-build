"""Trace the outline of a long object photographed square-on against a plain background.

For every image column it finds the top and bottom edge of the object, with a per-row background
model, so vignetting and gradients don't fool it. It median- and box-smooths both lines, then
converts pixels to metres:
  along  = (x - x0) * scale              (0 at your anchor column x0)
  top/bottom = (y_mid(x0) - y) * scale   (0 at the object's centre at x0, +up)
scale = length_m / (x1 - x0); x1 defaults to the last traced column (e.g. a blade tip).

  python -I trace_silhouette.py photo.jpg --x0 460 --length-m 0.48 --ymin 200 --ymax 520
  python -I trace_silhouette.py photo.jpg --x0 460 --length-m 0.48 --vertical     # object runs top->bottom

Writes <photo>_trace.json and <photo>_trace_debug.jpg (red = top, blue = bottom). Always look at the
debug image: if a line leaves the edge, change --threshold, --ymin/--ymax or crop the photo.
"""
import argparse, json, os, statistics
from PIL import Image, ImageDraw, ImageFilter

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("image")
ap.add_argument("--x0", type=int, required=True, help="anchor column (becomes along=0), e.g. a shoulder/joint")
ap.add_argument("--x1", type=int, help="column whose distance from x0 equals --length-m (default: last traced)")
ap.add_argument("--length-m", type=float, required=True)
ap.add_argument("--threshold", type=float, default=9.0, help="brightness difference from background")
ap.add_argument("--ymin", type=int, default=0)
ap.add_argument("--ymax", type=int, default=0, help="0 = image height")
ap.add_argument("--bg-strip", type=int, default=40, help="px width of the object-free strips at left/right")
ap.add_argument("--step", type=int, default=2)
ap.add_argument("--smooth", type=int, default=6, help="box-smoothing half-window in samples")
ap.add_argument("--vertical", action="store_true", help="object runs vertically; image is rotated first")
a = ap.parse_args()

src = Image.open(a.image)
if a.vertical:
    src = src.rotate(90, expand=True)
im = src.convert("L").filter(ImageFilter.GaussianBlur(1.2))
W, H = im.size
px = im.load()
ymax = a.ymax or H
B = a.bg_strip
L = [sum(px[x, y] for x in range(8, 8 + B)) / B for y in range(H)]
R = [sum(px[x, y] for x in range(W - B - 4, W - 4)) / B for y in range(H)]


def bg(x, y):
    t = x / (W - 1)
    return L[y] * (1 - t) + R[y] * t


cols = {}
for x in range(0, W, a.step):
    mask = [abs(px[x, y] - bg(x, y)) > a.threshold for y in range(H)]
    runs, start = [], None
    for y, m in enumerate(mask + [False]):
        if m and start is None:
            start = y
        elif not m and start is not None:
            runs.append((start, y - 1))
            start = None
    merged = []
    for r in runs:                                   # bridge tiny gaps (polished areas near bg value)
        if merged and r[0] - merged[-1][1] <= 6:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(r)
    merged = [r for r in merged if r[1] - r[0] >= 3 and a.ymin < r[0] < ymax]
    if merged and merged[-1][1] - merged[0][0] > 3:
        cols[x] = (merged[0][0], merged[-1][1])

xs = sorted(cols)
if not xs:
    raise SystemExit("nothing traced: lower --threshold or check --ymin/--ymax")
med = {}
for i, x in enumerate(xs):                           # median over 9 samples kills speckle
    win = xs[max(0, i - 4): i + 5]
    med[x] = (statistics.median(cols[k][0] for k in win), statistics.median(cols[k][1] for k in win))


def box(d, k):
    ks = sorted(d)
    out = {}
    for i, key in enumerate(ks):
        w = ks[max(0, i - k): i + k + 1]
        out[key] = sum(d[j] for j in w) / len(w)
    return out


top = box({x: med[x][0] for x in xs}, a.smooth)
bot = box({x: med[x][1] for x in xs}, a.smooth)

x0 = min(xs, key=lambda x: abs(x - a.x0))
x1 = a.x1 if a.x1 is not None else xs[-1]
S = a.length_m / (x1 - a.x0)
Y0 = (med[x0][0] + med[x0][1]) / 2
out = {
    "image": os.path.basename(a.image), "size": [W, H], "vertical": a.vertical,
    "scale_m_per_px": S, "anchor_px": [a.x0, Y0], "x1_px": x1, "length_m": a.length_m,
    "stations": [{"along": (x - a.x0) * S, "top": (Y0 - top[x]) * S, "bottom": (Y0 - bot[x]) * S} for x in xs],
}
base = os.path.splitext(a.image)[0]
json.dump(out, open(base + "_trace.json", "w"), indent=1)

dbg = src.convert("RGB")
d = ImageDraw.Draw(dbg)
d.line([(x, top[x]) for x in xs], fill=(255, 0, 0), width=2)
d.line([(x, bot[x]) for x in xs], fill=(0, 160, 255), width=2)
d.line([(a.x0, 0), (a.x0, H)], fill=(0, 200, 0), width=1)
dbg.save(base + "_trace_debug.jpg", quality=85)
print(f"traced {len(xs)} columns {xs[0]}..{xs[-1]}  scale {S:.6g} m/px  -> {base}_trace.json / _trace_debug.jpg")
