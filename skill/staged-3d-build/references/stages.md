# Stage playbook

Every stage: **Goal → Steps → Deliverables → Verify → Gate.** Don't start a stage until the one before it passes Verify.
Save `<Project>_v0N_<stage>.blend` at the end of each stage.

---
## 1. References for every angle
**Goal:** enough real views that no shape has to be guessed.
**Steps**
1. Build the view checklist from the target file. Every target needs: front, back, both sides, top, bottom, a ¾ view, plus close-ups of the hero detail and every secondary detail.
2. Gather the images:
   - **User's own:** read them.
   - **Public:** `python -I scripts/fetch_refs.py --query "..." --out refs`. Commons search; museum open-access images are CC0/PD. Group the filenames by part (`full_`, `detail_`, `hero_`, ...).
3. `python -I scripts/contact_sheet.py refs` and look at the sheet. Pick ONE **design set**, preferably one object shot from many angles, so all parts agree. Then pick a **trace source**: a clean silhouette on a plain background, shot square-on.
4. Set the real scale from known dimensions, a ruler in a photo, or published specs. If refs disagree in scale, take lengths/ratios from the design set and cross-sections from real-world standards, and write that decision down.
5. Trace: `python -I scripts/trace_silhouette.py <image> --length-m <real length> --x0 <px> --x1 <px>`. View the debug overlay, and fix the threshold or crop until the line hugs the edge.
6. Place the refs as image empties with `add_ref()`. Anchor each one to a **measured** pixel and verify against the traced mesh in front ortho with X-ray.

**Deliverables:** `refs/`, `refs/SOURCES.md` (file, title, URL, licence, author), contact sheet, trace JSON + overlay, a REF collection (hidden).
**Verify:** the trace overlay hugs the silhouette; the ref empty lines up with a test mesh within about 1 mm.

---
## 2. Blockout
**Goal:** correct proportions and placement of every part at real scale.
**Steps:**
- Define one coordinate convention (long axis, front face, origin at a meaningful joint) and a Z-stack/dimension table in `bl_lib.py`'s constants block.
- One script per assembly: loft cross-sections along traced profiles with `loft()` and `ellipse_ring()`.
- One object per real part, parented to a root empty, sorted into collections.

**Verify:** `look` front / side / ¾ against the refs; dimensions printed in cm.
**Gate:** pause for proportions (unless the user chose run-through).

---
## 3. Detail pass 1: silhouette + hero detail
**Goal:**
- every outline matches its ref;
- the repeated hero detail is exactly like the refs, built once and repeated.

**Steps**
1. Refine the outlines from the trace. Replace noisy trace ends with smooth analytic curves matched to the traced slope (tips, edges). Mark crisp lines as sharp edges.
2. **Study the hero detail first.** Crop the refs at full resolution, and use a ¾ view to tell the faces from the edges. Write down its rule in words: what repeats, the pitch, where the crossings and folds are, and what shows through.
3. **Build ONE unit:**
   - one full period of the pattern, in its own script, every dimension a named constant;
   - the ends must tile, so the last ring equals the first ring offset by one pitch;
   - give it its own UVs if it will be textured along its length.

   **Gate:** show the single unit, and a 3-copy preview so the user can see the tiling.
4. **Repeat it:**
   - an Array modifier (constant offset = pitch, merge on, UV offset per copy);
   - fit to the host shape with a Lattice whose points follow the host's real radii/axis;
   - trim the hidden ends with a Geometry Nodes Delete-by-position;
   - phase the pattern so no high point sits right at a fitting edge.
5. Continue in the stated direction (e.g. hilt → blade). Refine each fitting so it overlaps its neighbours by about 1 mm, with no gaps.

**Verify:**
- unit-level numbers (window size, band width, pitch);
- the array's vertex count;
- `look` close-ups next to the ref crops.

---
## 4. Detail pass 2: add
**Goal:** every secondary detail visible in the refs, listed and checked off.
**Steps:**
- Make a list from the refs: what, where, size, which face.
- Build each detail in a re-runnable script.
- Use booleans for holes and windows (`apply_boolean`). Recut from a freshly rebuilt base, never a second time.
- Where a detail pushes the hero detail (cord over an ornament), freeze the array with `freeze_modifiers` first. It keeps a hidden live `_UNIT` copy; displace the frozen copy.

**Verify:** `look` for each detail; check where parts must line up across objects (a hole and the part that passes through it).

---
## 5. Detail pass 3: refine + clean
- `bl_cleanup.py`:
  - hero parts must report 0 open edges;
  - intentionally open parts (trimmed ribbons) are listed as by design.
- **Fit checks:** contained parts inside containers (blade in scabbard, tang in grip), computed from the analytic sections and printed.
- Smooth by angle (30°) on every part; sharp edges stay marked.
- Clean names, collections, applied scale. The live units and lattices stay hidden.

---
## 6. UVs
- Use one texture set per material family (e.g. blade / fittings / grip / scabbard / hero detail).
- Strip-like parts (cords, ribbons, straps) get UVs at build time: u along the length, v around. Everything else gets smart-projected per object (66°; about 20° for tubes), then average-scaled and packed per set.
- Run `bl_uv_overlap_check.py`. Each set must be about 0 px (≤ 0.01% is edge-touching). Export the layout PNGs to `renders/`.

---
## 7. Texturing: wear + realism
- **One material per surface type.** Start from physically sensible base values, and keep dark materials dark (lacquer ≈ 0.1 albedo, black cord ≈ 0.01–0.02).
- **Wear goes where physics puts it:**
  - **AO:** dirt, patina and rust in crevices.
  - **Pointiness:** rubbed, polished edges, and chips on exposed edges.
  - **Noise:** breaks up every mask.
- Patterns that follow geometry (temper lines, stripes, grain) come from **mesh attributes** written by script (e.g. a 0→1 distance from an edge), or from object coordinates along the long axis.
- **Test renders:** do them in Cycles at 50% resolution and about 48 samples. Judge them after viewing; fix exposure first, then colour.

---
## 8. Look-dev + renders
- `bl_lookdev_studio.py`:
  - display pose resting on the floor (contact shadows);
  - 3-point area rig at about ⅓ of the usual watts for small objects;
  - a reflection card placed on the camera's mirror ray for polished surfaces, hidden from camera;
  - a dark backdrop, a hero camera, and detail cameras.
- `blender-look-dev`, if installed, for mood choices.
- **Finals:** 1920×1080, 96–128 samples, denoise. Renders over 120 s detach the MCP call, so check that the file exists.
- Compare against the refs and list the remaining weaknesses honestly.

---
## 9. Output
- `.blend` only: final save plus stage snapshots.
- Web: `references/target-web.md`.
- Roblox: `references/target-roblox.md`.
- Close with: a session log (what was done, decisions, next steps, the script run order) and a commit.
