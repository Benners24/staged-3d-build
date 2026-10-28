"""Blender helpers for staged builds. Copy into <Project>/scripts/ and exec() at the top of every part script:

    exec(open(r"<Project>/scripts/bl_lib.py", encoding="utf-8").read())

Put the project's coordinate convention and dimension constants in the CONFIG block below
(e.g. long axis = +Z, front face = -Y, origin at a joint; metres).
"""
import bpy, bmesh, json, math, os
from mathutils import Vector, Matrix

# ---- CONFIG (edit per project) ----------------------------------------------------------
PROJECT = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.path.expanduser("~/Documents/Blender/Project")
REFS = os.path.join(PROJECT, "refs")
ROOT_NAME = "ROOT"            # empty that parents every part (create it in the setup script)
# dimension table / Z-stack constants go here


# ---- interpolation ------------------------------------------------------------------------
def interp(stations, key, x, along="along"):
    """Linear interpolation of stations[key] at position x (stations sorted by `along`, None skipped)."""
    pts = [(s[along], s[key]) for s in stations if s.get(key) is not None]
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    lo, hi = 0, len(pts) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if pts[mid][0] <= x:
            lo = mid
        else:
            hi = mid
    (x0, v0), (x1, v1) = pts[lo], pts[hi]
    return v0 + (v1 - v0) * ((x - x0) / (x1 - x0) if x1 != x0 else 0)


def smoothstep(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


# ---- objects ------------------------------------------------------------------------------
def collection(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def replace_object(name):
    """Delete an object (and its now-unused mesh) so scripts are re-runnable."""
    ob = bpy.data.objects.get(name)
    if ob:
        me = ob.data if ob.type == 'MESH' else None
        bpy.data.objects.remove(ob, do_unlink=True)
        if me and me.users == 0:
            bpy.data.meshes.remove(me)


def finish_object(bm, name, coll_name, smooth=False, merge=1e-6):
    """bmesh -> fresh object in a collection, parented to ROOT_NAME (if present), normals fixed."""
    replace_object(name)
    if merge:
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    collection(coll_name).objects.link(ob)
    root = bpy.data.objects.get(ROOT_NAME)
    if root:
        ob.parent = root
    for p in me.polygons:
        p.use_smooth = smooth
    return ob


# ---- geometry builders ----------------------------------------------------------------------
def loft(bm, rings, cap_start=True, cap_end=True, tip_start=None, tip_end=None):
    """Bridge closed rings (equal-length lists of Vector). Optional single tip vertex at either end.
    Returns the vertex rings (use them to mark sharp edges or set UVs)."""
    vrings = [[bm.verts.new(p) for p in r] for r in rings]
    n = len(rings[0])
    for a, b in zip(vrings, vrings[1:]):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((a[i], a[j], b[j], b[i]))
    if tip_start is not None:
        t = bm.verts.new(tip_start)
        for i in range(n):
            bm.faces.new((vrings[0][(i + 1) % n], vrings[0][i], t))
    elif cap_start:
        bm.faces.new(list(reversed(vrings[0])))
    if tip_end is not None:
        t = bm.verts.new(tip_end)
        for i in range(n):
            bm.faces.new((vrings[-1][i], vrings[-1][(i + 1) % n], t))
    elif cap_end:
        bm.faces.new(vrings[-1])
    return vrings


def ellipse_ring(cx, cz, rx, ry, n, y0=0.0, power=2.0):
    """Superellipse ring in the XY plane at height cz (power > 2 = boxier, 2 = ellipse)."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        pts.append(Vector((cx + math.copysign(abs(c) ** (2 / power), c) * rx,
                           y0 + math.copysign(abs(s) ** (2 / power), s) * ry, cz)))
    return pts


def mark_sharp_along(bm, vrings, indices):
    """Mark the lengthwise edges at ring positions `indices` as sharp (ridges, edges, creases)."""
    for a, b in zip(vrings, vrings[1:]):
        for j in indices:
            e = bm.edges.get((a[j], b[j]))
            if e:
                e.smooth = False


# ---- reference images ----------------------------------------------------------------------
AXES = {"X": Vector((1, 0, 0)), "-X": Vector((-1, 0, 0)), "Y": Vector((0, 1, 0)), "-Y": Vector((0, -1, 0)),
        "Z": Vector((0, 0, 1)), "-Z": Vector((0, 0, -1))}


def add_ref(name, filename, m_per_px, anchor_px, anchor_world, image_right="X", image_up="Z",
            squash_up=1.0, opacity=0.5):
    """Place a photo as an image empty so pixel `anchor_px` lands exactly on `anchor_world` (Vector).
    image_right / image_up: which world axes the photo's +x and up directions map to, e.g.
    front view of an upright object: ("X", "Z"); a long object lying along +Z seen from the front: ("Z", "X").
    Verify afterwards: mesh vs ref in ortho view with X-ray."""
    replace_object(name)
    img = bpy.data.images.get(filename) or bpy.data.images.load(os.path.join(REFS, filename))
    W, H = img.size
    u, v = AXES[image_right], AXES[image_up]
    rot = Matrix((u, v, u.cross(v))).transposed()          # columns = where local X, Y, Z go
    ob = bpy.data.objects.new(name, None)
    ob.empty_display_type = 'IMAGE'
    ob.data = img
    ob.empty_display_size = max(W, H) * m_per_px
    ob.empty_image_offset = (0.0, 0.0)
    ob.color[3] = opacity
    ob.rotation_euler = rot.to_euler()
    ob.scale = (1.0, squash_up, 1.0)
    local = Vector((anchor_px[0] * m_per_px, (H - anchor_px[1]) * m_per_px * squash_up, 0.0))
    ob.location = Vector(anchor_world) - rot @ local
    ob.hide_select = True
    collection("REF").objects.link(ob)
    return ob


# ---- modifiers ------------------------------------------------------------------------------
def _bake_evaluated(ob):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)
    me.name = ob.name
    return ob


def apply_boolean(ob, cutter, operation='DIFFERENCE', delete_cutter=True, smooth=True):
    """Apply a boolean for real (exact solver) and remove the cutter. Recut from a fresh base on re-runs."""
    mod = ob.modifiers.new("bool", 'BOOLEAN')
    mod.operation, mod.solver, mod.object = operation, 'EXACT', cutter
    _bake_evaluated(ob)
    if smooth:
        for p in ob.data.polygons:
            p.use_smooth = True
    if delete_cutter:
        replace_object(cutter.name)
    return ob


def freeze_modifiers(name):
    """Make `name` a plain mesh evaluated from a hidden live copy `<name>_UNIT` (kept with its modifiers).
    First call creates the unit; later calls re-evaluate it, so edits never stack."""
    src = bpy.data.objects[name]
    unit = bpy.data.objects.get(name + "_UNIT")
    if unit is None:
        unit = src.copy()
        unit.data = src.data.copy()
        unit.name = name + "_UNIT"
        for c in src.users_collection:
            c.objects.link(unit)
    unit.hide_viewport = False
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(unit.evaluated_get(dg))
    unit.hide_viewport = unit.hide_render = True
    old = src.data
    src.modifiers.clear()
    src.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)
    me.name = name
    return src


def view3d_override():
    area = next(a for a in bpy.context.screen.areas if a.type == 'VIEW_3D')
    return bpy.context.temp_override(area=area, region=next(r for r in area.regions if r.type == 'WINDOW'))


def auto_smooth(ob, angle_deg=30):
    """Smooth-by-angle (Blender 4.1+); keeps marked sharp edges crisp, removes cap streaks."""
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]):
        bpy.ops.object.shade_auto_smooth(angle=math.radians(angle_deg))
