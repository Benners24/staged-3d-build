"""Stage 6 check: rasterise every UV triangle of each texture set and count pixels covered twice.
This is the authority for "no overlaps" (Blender 5.x scripted uv.select_overlap counts are unreliable).

Set before exec (optional):
    GROUPS = {"blade": ["BLADE", "HABAKI"], ...}   # default: one set per first material name
    RES = 1024
Edge-touching islands give a handful of px; aim for <= 0.01 % per set.
"""
import bpy
import numpy as np

RES = globals().get("RES", 1024)
GROUPS = globals().get("GROUPS")
if not GROUPS:
    GROUPS = {}
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.visible_get() and o.data.uv_layers and not o.name.startswith(("LD_", "_")):
            key = o.data.materials[0].name if o.data.materials and o.data.materials[0] else "no_material"
            GROUPS.setdefault(key, []).append(o.name)


def overlap_pixels(names):
    count = np.zeros((RES, RES), dtype=np.uint16)
    for n in names:
        me = bpy.data.objects[n].data
        if not me.uv_layers:
            print("  (no UVs)", n)
            continue
        me.calc_loop_triangles()
        uv = np.empty(len(me.loops) * 2, dtype=np.float32)
        me.uv_layers.active.data.foreach_get("uv", uv)
        uv = uv.reshape(-1, 2) * RES
        tris = np.empty(len(me.loop_triangles) * 3, dtype=np.int32)
        me.loop_triangles.foreach_get("loops", tris)
        for a, b, c in uv[tris.reshape(-1, 3)]:
            x0 = max(int(np.floor(min(a[0], b[0], c[0]))), 0)
            x1 = min(int(np.ceil(max(a[0], b[0], c[0]))), RES)
            y0 = max(int(np.floor(min(a[1], b[1], c[1]))), 0)
            y1 = min(int(np.ceil(max(a[1], b[1], c[1]))), RES)
            if x1 <= x0 or y1 <= y0:
                continue
            d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(d) < 1e-12:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
            l1 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / d
            l2 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / d
            count[y0:y1, x0:x1] += (l1 > 0) & (l2 > 0) & (1 - l1 - l2 > 0)
    return int((count > 1).sum()), int((count > 0).sum())


for tag, names in GROUPS.items():
    over, used = overlap_pixels(names)
    pct = 100 * over / max(used, 1)
    print(f"{tag:14s} overlap px {over:7d} / used {used:8d}  ({pct:.3f}%)  {'OK' if pct <= 0.01 else 'FIX'}")
