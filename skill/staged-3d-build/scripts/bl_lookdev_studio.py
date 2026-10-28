"""Stage 8 studio: 3-point area rig, a reflection card on the camera's mirror ray (hidden from camera),
dark curved backdrop at z=0, hero camera + optional detail cameras, Cycles on the GPU with AgX.
Everything created is prefixed LD_ and lives in a LOOKDEV collection (safe to re-run).

Pose the model first (resting on z = 0). Optional settings before exec:
    POWER_SCALE = 1.0        # all light watts x this (defaults are tuned for ~0.5-1 m objects)
    CAM_ELEV = 38            # hero camera elevation in degrees
    DETAILS = [("Hilt", (x, y, z), 0.35, 42, -12), ...]   # name, world point, distance, elevation, azimuth
    CARD = True              # reflection strip for polished metal / lacquer
"""
import bpy, bmesh, math
from mathutils import Vector

POWER_SCALE = globals().get("POWER_SCALE", 1.0)
CAM_ELEV = globals().get("CAM_ELEV", 38)
DETAILS = globals().get("DETAILS", [])
CARD = globals().get("CARD", True)
sc = bpy.context.scene

pts = [o.matrix_world @ Vector(c) for o in bpy.data.objects
       if o.type == 'MESH' and o.visible_get() and not o.name.startswith(("LD_", "REF_", "_"))
       for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
center, size = (lo + hi) / 2, max(hi - lo)

LD = bpy.data.collections.get("LOOKDEV") or bpy.data.collections.new("LOOKDEV")
if LD.name not in sc.collection.children:
    sc.collection.children.link(LD)


def ld_obj(name, data):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    ob = bpy.data.objects.new(name, data)
    LD.objects.link(ob)
    return ob


def view_from(c, dist, elev, az=0.0):
    e, a = math.radians(elev), math.radians(az)
    return c + Vector((dist * math.cos(e) * math.sin(a), -dist * math.cos(e) * math.cos(a), dist * math.sin(e)))


def material(name, setup):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    setup(m.node_tree)
    return m


target = ld_obj("LD_Target", None)
target.location = center


def area_light(name, watts, size_, loc, color=(1, 1, 1), size_y=None):
    ld = bpy.data.lights.get(name) or bpy.data.lights.new(name, 'AREA')
    ld.energy, ld.color, ld.shape, ld.size = watts * POWER_SCALE, color, 'RECTANGLE', size_
    ld.size_y = size_y or size_
    ob = ld_obj(name, ld)
    ob.location = loc
    con = ob.constraints.new('TRACK_TO')
    con.target, con.track_axis, con.up_axis = target, 'TRACK_NEGATIVE_Z', 'UP_Y'
    return ob


D = 2.5 * size
area_light("LD_Key", 80, 0.5 * size, center + Vector((-0.55 * D, -0.75 * D, 0.65 * D)), (1.0, 0.96, 0.9))
area_light("LD_Fill", 22, 0.6 * size, center + Vector((0.7 * D, -0.6 * D, 0.15 * D)), (0.9, 0.95, 1.0))
area_light("LD_Rim", 110, 0.4 * size, center + Vector((0.2 * D, 0.9 * D, 0.7 * D)))

# world + backdrop
w = sc.world or bpy.data.worlds.new("LD_World")
sc.world = w
try:
    w.use_nodes = True
except Exception:
    pass
bgn = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
bgn.inputs['Color'].default_value = (0.012, 0.012, 0.014, 1)

bm = bmesh.new()
W_, y_back, R = 3.0 * size, center.y + 0.9 * size, 0.25 * size
rows = []
for k in range(13):                                  # floor -> curve -> wall
    if k < 4:
        y, z = center.y - 1.5 * size + (y_back - R - (center.y - 1.5 * size)) * k / 3, 0.0
    elif k < 12:
        a = (math.pi / 2) * (k - 4) / 7
        y, z = y_back - R + R * math.sin(a), R - R * math.cos(a)
    else:
        y, z = y_back, 1.2 * size
    rows.append([bm.verts.new((center.x + x, y, z)) for x in (-W_ / 2, W_ / 2)])
for a_, b_ in zip(rows, rows[1:]):
    bm.faces.new((a_[0], a_[1], b_[1], b_[0]))
me = bpy.data.meshes.new("LD_Backdrop")
bm.to_mesh(me)
bm.free()
for p in me.polygons:
    p.use_smooth = True


def grey(nt):
    pb = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    pb.inputs['Base Color'].default_value = (0.035, 0.033, 0.031, 1)
    pb.inputs['Roughness'].default_value = 0.65


me.materials.append(material("LD_Backdrop", grey))
ld_obj("LD_Backdrop", me)

# hero camera
cams = []


def camera(name, loc, look_at, lens=85):
    cd = bpy.data.cameras.get(name) or bpy.data.cameras.new(name)
    cd.lens, cd.clip_start = lens, 0.005
    ob = ld_obj(name, cd)
    ob.location = loc
    ob.rotation_euler = (Vector(look_at) - Vector(loc)).normalized().to_track_quat('-Z', 'Y').to_euler()
    cams.append(name)
    return ob


main = camera("LD_Cam_Main", view_from(center, 2.6 * size, CAM_ELEV), center)
for name, p, dist, elev, az in DETAILS:
    camera("LD_Cam_" + name, view_from(Vector(p), dist, elev, az), p)
sc.camera = main

# reflection strip where the hero camera's mirror ray (off a floor-facing surface) goes
if CARD:
    cbm = bpy.data.meshes.new("LD_Card")
    b2 = bmesh.new()
    hx, hy = 1.1 * size, 0.16 * size
    b2.faces.new([b2.verts.new((x, y, 0)) for x, y in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))])
    b2.to_mesh(cbm)
    b2.free()

    def emit(nt):
        nt.nodes.clear()
        em, mo = nt.nodes.new('ShaderNodeEmission'), nt.nodes.new('ShaderNodeOutputMaterial')
        em.inputs['Strength'].default_value = 1.2
        nt.links.new(em.outputs[0], mo.inputs[0])

    cbm.materials.append(material("LD_Card", emit))
    card = ld_obj("LD_Card", cbm)
    e = math.radians(CAM_ELEV)
    card.location = center + Vector((0, math.cos(e), math.sin(e))) * 1.45 * size
    card.rotation_euler = (center - card.location).normalized().to_track_quat('Z', 'Y').to_euler()
    card.visible_camera = False

# Cycles on the GPU
try:
    sc.render.engine = 'CYCLES'
except TypeError as err:
    print("engine:", err)
prefs = bpy.context.preferences.addons['cycles'].preferences
for dev in ('OPTIX', 'CUDA', 'HIP', 'METAL', 'ONEAPI'):
    try:
        prefs.compute_device_type = dev
        prefs.get_devices()
        if any(d.type == dev for d in prefs.devices):
            for d in prefs.devices:
                d.use = d.type == dev
            sc.cycles.device = 'GPU'
            break
    except TypeError:
        continue
sc.cycles.samples, sc.cycles.use_denoising = 128, True
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
try:
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.view_settings.exposure = -0.3
except TypeError as err:
    print("view:", err)
print(f"look-dev ready: size {size:.3f} m, cameras {cams}, device {sc.cycles.device}")
