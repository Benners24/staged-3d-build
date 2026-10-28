# Lessons (pitfalls with fixes)

| Symptom | Cause | Fix |
|---|---|---|
| Hand-placed outline doesn't match the ref | eyeballed points | Trace from pixels (`trace_silhouette.py`) and overlay the trace on the photo before modelling |
| Ref image empty sits centimetres off-axis | anchor pixel read from a downscaled crop | Measure the anchor with a pixel scan; check the mesh against the ref in front ortho with X-ray |
| Two refs disagree in scale | different objects or crops | Lengths/ratios from the design set, cross-sections from real-world standards; write the decision down |
| Repeated detail (wrap/braid) looks wrong or won't centre | modelled as one long helix/procedure | Model ONE period with an explicit profile (where it rises, where it crosses), then Array + Lattice + GN trim |
| Array copies overlap in UV space | unit UVs copied as-is | Give the unit UVs in a band; Array `offset_u` / `offset_v` = band size |
| Re-running a script doubles a bulge or cut | edits applied to an already-edited mesh | Freeze from a hidden live `_UNIT` copy; recut booleans on a freshly rebuilt base |
| Boolean result not kept | modifier never applied | `apply_boolean()` → `new_from_object` on the evaluated mesh, then delete the cutter |
| Tip/end looks blunt or flat-topped | trace noisy in the last pixels | Analytic Hermite end, slope matched to the trace at the join |
| Radial streaks on flat discs | smooth shading over n-gon caps | `auto_smooth(30°)` |
| `uv.select_overlap` reports thousands of overlaps | Blender 5.x UV selection lives in the `.uv_select_face` attribute; scripted selection is unreliable | Use `bl_uv_overlap_check.py` (raster) as the authority |
| Tube-like part has folded UV islands | smart project at 66° on a tube | Re-project that object alone at about 20°, or give it strip UVs when you build it |
| First Cycles render takes minutes | OptiX kernel compile | Wait once; later renders are fast |
| MCP says "No data received" during a render | call over 120 s detaches | The render usually finished: check the output file |
| "cannot save" a render | file open/locked elsewhere | Write to a new filename |
| Whole render washed out, dark colours pastel | light watts tuned for metre-scale scenes | Small objects: about ⅓ the usual watts; dark world/backdrop; AgX, exposure −0.3 |
| Polished blade renders black / hamon invisible | nothing bright on the mirror ray | Emissive card (hidden from camera) placed where the camera's reflection ray goes; keep it a strip so the rest stays dark |
| Objects float in the render | display pose not grounded | Rest everything on z=0 (flat lay) or model a stand |
| Wikimedia HTTP 429 | too many requests | Backoff + delay (built into `fetch_refs.py`); delete 0-byte partial files with `find refs -type f -size 0 -delete` (never `find refs -size 0`) |
| Blender UI ops fail in scripts | no area context | `bpy.context.temp_override(area=VIEW_3D, region=WINDOW)` |
| Context breaks mid-script | `read_homefile` | Never call it; clear objects with `bpy.data.objects.remove` |
