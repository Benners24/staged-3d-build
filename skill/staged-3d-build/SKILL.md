---
name: staged-3d-build
description: Use when asked to build, make, model or "test build" a 3D prop, weapon, vehicle part, character, creature, or Roblox avatar/UGC item in Blender from references, especially when the request mentions references for each angle, blockout, detail passes, a repeated detail (wrap, braid, plates, stitches), wear, texturing, realism, or stage-by-stage work.
---

# Staged 3D Build

## Overview
A model built in fixed stages, each one verified against references before the next starts, ends up matching the reference. Cleanup is not left to the end. Plan the whole build first (plan mode), then execute stage by stage. Each stage has its own deliverable, a check and a save.

Works through the live Blender MCP (`execute_blender_code`, `look`). Single-image tracing is covered in depth by `blender-reference-model`, if installed.

## Stage 0: Intake and plan (always, in plan mode)
1. Fill every field of `PROMPT_TEMPLATE.md` (in this skill's folder) from the request. Ask only the decisions that change the work, with one recommended option each:
   - **target type:** read `references/target-<type>.md`;
   - **scope:** extra pieces, e.g. scabbard, stand, cape;
   - **style variant of the hero detail:** e.g. wrap style, braid type;
   - **output use:** render / web GLB / Roblox;
   - **reference source:** gather / user's own;
   - **gates:** pause at the blockout and the hero unit, or run straight through after plan approval.
2. Check Blender (read-only) before asking anything: `get_addon_status`, `get_scene_info`. Note the version, add-ons, GPU, and enabled asset libraries.
3. Put these in the first question batch, each with a recommended answer:
   - project folder (recommend `~/Documents/Blender/<Project>`);
   - pose (A-pose or T-pose) and triangle budget, for characters and Roblox;
   - whether the user has their own concept art or references.
4. Write the plan: Context, Project layout, Stages 1–9 with deliverables, Verification. Exit plan mode. Plan approval counts as approval to create the folder and the files named in the plan. Ask again for anything outside it.
5. On approval:
   - create `<Project>/refs, scripts, textures, renders`;
   - copy `scripts/bl_lib.py` into the project's `scripts/`;
   - save `<Project>.blend`.

**Quick path:** if the request says quick, fast, today, or "don't overthink it", follow the Quick path section below instead of the full stage list.

## Stages (details, checks and gates: `references/stages.md`)
| # | Stage | Deliverable | Gate (default) |
|---|---|---|---|
| 1 | References for every angle | `refs/` + `SOURCES.md` + contact sheet + chosen design set + measured scale + ref empties | — |
| 2 | Blockout at real scale | one object per part, collections, `_v01_block.blend` | **pause: proportions** |
| 3 | Detail pass 1: silhouette + hero detail | refined outlines; ONE hero unit → array/instance → fit; work in the stated direction | **pause: hero unit** |
| 4 | Detail pass 2: add | secondary details listed from refs | — |
| 5 | Detail pass 3: refine + clean | 0 open edges on hero parts, fits checked, smoothing, names | — |
| 6 | UVs | every texture set: raster overlap ≈ 0, layout PNGs | — |
| 7 | Texturing: wear + realism | one material per surface type, AO/Pointiness/attribute masks | — |
| 8 | Look-dev + renders | lights, cameras, final renders, honest comparison against refs | — |
| 9 | Output | `.blend` / baked GLB (`references/target-web.md`) / Roblox checks (`references/target-roblox.md`) | — |

If the user says to keep going ("go on from now"), drop the remaining pauses but keep every check.

## Quick path (for "quick", "today", "don't overthink it")
Say up front what is shortened and what outside delays remain (for example marketplace review, a client sign-off). Then:
1. **One question batch**, 3 questions at most, each with a recommended answer. If the user says "just go", use the recommendations.
2. **References:** 3–5 images of one object, or the user's own. Skip the trace unless a long profile needs it.
3. **Blockout + hero unit together**, then ONE pause showing both.
4. **Merge detail passes 2 and 3** into one pass. Run `bl_cleanup.py` at the end of it.
5. **UVs + wear in one step.** Wear stays at the two mask types (AO for crevices, Pointiness for edges).
6. **One hero render** plus one close-up.

**Never shortened, even on the quick path:**
- the hero detail is built as ONE unit and repeated, never modelled as one long shape;
- numeric checks (dimensions, open edges, triangle count, spec limits);
- `bl_uv_overlap_check.py`;
- the target's spec limits (Roblox, web).

## Working rules
- **Every part comes from a re-runnable script in `<Project>/scripts/`.** Each script begins `exec(open(".../bl_lib.py").read())` and replaces its own objects. Re-running a script must never stack edits; rebuild from source objects.
- **After every step:** `look` at the result, plus numbers (dimensions, open edges, overlap px). Name mismatches against the refs honestly.
- **Saves:** an incremental `.blend` per stage (`_v0N_<stage>`), plus a session log and commit at major boundaries or about 50% context.
- **Show the code** being run, and explain each stage in plain words before starting it.
- **Companion skills, if installed:** `blender-look-dev` (stage 8), `blender-web-export` (stage 9), `roblox-character-blender` (Roblox specs), `commit-vault` (checkpoints).

## Tools (`scripts/`)
| Script | Run with | Use |
|---|---|---|
| `fetch_refs.py` | `python -I scripts/fetch_refs.py --help` | Wikimedia Commons search/download with backoff, writes `SOURCES.md` |
| `contact_sheet.py` | `python -I` | labelled tile sheet of `refs/` |
| `trace_silhouette.py` | `python -I` | pixel-traced outline (top/bottom edge per column) → JSON in metres |
| `bl_lib.py` | exec in Blender | loft, rings, finish_object, add_ref, apply_boolean, freeze_modifiers, auto_smooth |
| `bl_cleanup.py` | exec in Blender | doubles, loose, normals, open-edge report |
| `bl_uv_overlap_check.py` | exec in Blender | raster UV overlap per texture set |
| `bl_lookdev_studio.py` | exec in Blender | 3-point rig, reflection card, backdrop, cameras, Cycles GPU |

## Common mistakes
See `references/lessons.md`. The expensive ones:
- **Tracing by eye.** Trace from pixels and verify anchors numerically.
- **Modelling the repeated detail as one long procedural shape.** Build one unit, then array it.
- **Trusting a scripted `uv.select_overlap` in Blender 5.x.** Use the raster check instead.
- **Rendering a polished metal object without a reflection source.**
