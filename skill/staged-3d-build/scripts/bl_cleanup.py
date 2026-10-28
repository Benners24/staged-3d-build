"""Stage 5 hygiene: merge doubles, drop loose verts, fix normals, smooth by angle, report open edges.

Set before exec (optional):
    PARTS = ["BLADE", ...]          # default: every visible mesh not starting with LD_ / REF_ / _
    OPEN_BY_DESIGN = {"WRAP"}        # parts allowed to have open edges (trimmed ribbons etc.)
    SMOOTH_ANGLE = 30
Hero parts should report 0 open edges.
"""
import bpy, bmesh, math

PARTS = globals().get("PARTS") or [o.name for o in bpy.data.objects
                                   if o.type == 'MESH' and o.visible_get()
                                   and not o.name.startswith(("LD_", "REF_", "_")) and not o.name.endswith("_UNIT")]
OPEN_BY_DESIGN = globals().get("OPEN_BY_DESIGN", set())
SMOOTH_ANGLE = globals().get("SMOOTH_ANGLE", 30)

rows, problems = [], []
for name in PARTS:
    ob = bpy.data.objects[name]
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    before = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    loose = [v for v in bm.verts if not v.link_edges]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    open_edges = sum(1 for e in bm.edges if not e.is_manifold)
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()
    if not any(m.type == 'NODES' and 'Smooth' in m.name for m in ob.modifiers):
        with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]):
            bpy.ops.object.shade_auto_smooth(angle=math.radians(SMOOTH_ANGLE))
    flag = "  (by design)" if name in OPEN_BY_DESIGN else ""
    if open_edges and not flag:
        problems.append(name)
    rows.append(f"{name:16s} verts {len(ob.data.vertices):7d}  merged {before - len(ob.data.vertices):4d}  "
                f"loose {len(loose):3d}  open-edges {open_edges:5d}{flag}")
print("\n".join(rows))
print("NEEDS ATTENTION:", problems if problems else "none")
