# Target: characters and creatures

## Reference checklist
- **Turnaround:** front, side, back (and ¾) at the same scale, in a neutral A- or T-pose. Without a true turnaround, collect matching front and side shots and align them by eye height, chin, shoulders, crotch and knees.
- **Close-ups:** face (front and profile), hands, feet, hair from several angles, and every costume detail (seams, buckles, folds, patterns).
- **Proportion data:** height, plus heads-tall; e.g. about 7.5 for realistic adults, 2–4 for stylized/chibi.

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
  - apply the Mirror (unless UVs stay mirrored to save space);
  - check the rest pose is symmetric;
  - check normals and open edges;
  - check that clothing doesn't intersect the body (offset ≥ 1 mm);
  - check scale is 1 and the origin is at the feet.
- **UVs:** seams hidden (inner arms, inner legs, behind the hairline, under the clothing). The face gets the largest texel density.
- **Texturing:**
  - skin: subsurface 0.1–0.2, roughness 0.45–0.55, with AO darkening in creases;
  - cloth: sheen 0.3–0.6 with a weave bump, plus dirt at hems and edges;
  - metal trims: the props wear rules apply.
- **Output:** rig-ready if asked. Clean A/T-pose, applied transforms, named parts. Rigging itself is a separate task unless requested.

## Pitfalls
- Front and side refs at different scales or heights. Measure both against the same landmarks before modelling.
- Modelling the clothing fused to the body. Keep separate shells so they can be layered or swapped.
- Joints without supporting loops. They collapse once rigged.
