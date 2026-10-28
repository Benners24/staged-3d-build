# Target: characters and creatures

## Reference checklist
- **Turnaround:** front, side, back (and ¾) at the same scale, in a neutral A- or T-pose. Without a true turnaround, collect matching front and side shots and align them by eye height, chin, shoulders, crotch and knees.
- **Close-ups:** face (front and profile), hands, feet, hair from several angles, and every costume detail (seams, buckles, folds, patterns).
- **Proportion data:** height, plus heads-tall; e.g. about 7.5 for realistic adults, 2–4 for stylized/chibi.

## Stylized characters (no turnaround, or between standard proportions)
- Agree a written proportion sheet before modelling: height, heads-tall (6 sits between realistic ~7.5 and chibi 2–4), and which parts are exaggerated (hands, feet, shoulders).
- Pose and budget are Stage 0 questions: A-pose is the default for rigging, and the triangle budget comes from the use (render / game / web).

## Rigging rules for repeated geometry (mail, scales, plates)
- **The rigged mesh is the base shell.** Rings or scales are an instancing layer on top of it, never the thing that gets weighted.
- Pick one of two outputs and say which in the plan:
  1. **Baked:** normal + opacity + AO maps on the shell. Best for animation and game/web. The shell stays light and deforms cleanly.
  2. **Instanced:** keep the Geometry Nodes setup live, parented to the shell, with instances following the shell surface. Best for close-up renders. Apply it only for a still.
- Modifier order on rigged parts: Armature last; Mirror already applied; no Array/GN modifiers on the weighted mesh itself.
- Rigid pieces (pauldron plates, buckles) attach whole to one bone; keep them separate objects.

## Baking a repeated surface (mail, scales) to maps
Preferred (small, tileable): bake ONE cell, then tile it.
1. Build one cell as real geometry on a flat plane with the cell's tile size; give the plane a UV that fills 0–1 exactly.
2. In Cycles, bake onto that plane from the cell geometry (selected-to-active, small ray distance): Normal (tangent), AO, and an opacity map (give the rings a white emission and the background black, then bake the Emit pass).
3. Put the maps on the shell's material and set the UV scale so one tile matches the real ring size. Check the ring size in cm against the ref.

Fallback (whole-surface bake): instance the cell over the shell, bake selected-to-active from the instanced copy to the shell's unique UVs, then delete the copy. This costs a large texture, so use it only when the surface pattern must follow the body (decals, damage).

Triangle budget for a rigged character: set it in Stage 0 from the use (render: no hard cap; game/web: agree a number with the user), write it down, and keep a running count per part at every stage.

## Stage notes
- **References:**
  - place the front ref on the XZ plane and the side ref on the YZ plane;
  - line up the feet at Z=0;
  - put the centre line exactly on X=0;
  - write a proportion sheet (height, head, shoulder, hip, knee, elbow and wrist heights).
- **Blockout:** model only the right half (+X) with a Mirror modifier (clipping, merge). Use simple lofted segments for the torso, limbs and head, at the proportion-sheet heights. Keep the clothing as separate shells.
- **Detail pass 1:**
  - refine the silhouette from front and side at the same time;
  - add **deformation loops**: 3 loops around shoulders, elbows, wrists, hips, knees and ankles; mouth and eye rings and a nasolabial loop on the face;
  - keep it quad-dominant with poles away from joints.

  The hero detail is a repeated costume or anatomy element: a braid segment, chain link, armor plate, scale, stitch, or button row. Build one unit, then Array/instance + Curve/Lattice along the body.
- **Detail pass 2:**
  - hands: fingers lofted from rings, knuckle loops;
  - face: features;
  - accessories.

  Hair uses **real meshes or hair cards**, not scripted strands. If a matching hair asset exists, fit it.
- **Detail pass 3:**
  - apply the Mirror before any weighting (always);
  - check the rest pose is symmetric;
  - check normals and open edges;
  - check that clothing doesn't intersect the body (offset ≥ 1 mm);
  - check scale is 1 and the origin is at the feet.
- **UVs:** unique (non-overlapping) by default, so wear can differ left and right. If the user chooses mirrored UV halves to save texture space, list those mirrored pairs as the only allowed overlap and exclude them from the overlap check. Seams hidden (inner arms, inner legs, behind the hairline, under the clothing). The face gets the largest texel density.
- **Texturing:**
  - skin: subsurface 0.1–0.2, roughness 0.45–0.55, with AO darkening in creases;
  - cloth: sheen 0.3–0.6 with a weave bump, plus dirt at hems and edges;
  - metal trims: the props wear rules apply.
- **Output:** rig-ready if asked. Clean A/T-pose, applied transforms, named parts. Rigging itself is a separate task unless requested.

## Pitfalls
- Front and side refs at different scales or heights. Measure both against the same landmarks before modelling.
- Modelling the clothing fused to the body. Keep separate shells so they can be layered or swapped.
- Joints without supporting loops. They collapse once rigged.
