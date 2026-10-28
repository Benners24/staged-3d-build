# Example run: wakizashi (Japanese short sword) with saya

## The original request
> test build make a Wakizashi. Look up references for each angles. Once you gathered reference
> proceed with the blocking of the shape then add the first out of 3 detail pass. 1st is refine
> the silhoette the wrappping of the handle has to be precise like how they wrapped it, work out
> the first wrap then array it, then moving from the hilt to the blade. The rest of the detail
> pass is just furthur to add, refine, and clean details. Next is texturing for some wear and realism

## The same request as a filled template
```
Build a weapon — wakizashi (Edo-period Japanese short sword).
Use: high-detail render   Include: sword + saya (scabbard)   Exclude: stand
References: gather public-domain/CC museum photos — every angle + close-ups of the handle wrap,
  tsuba, kissaki (tip), habaki, saya fittings.
Real size: derive from refs (nagasa ~48 cm).
Stages:
1. References for each angle → ONE design set + a clean bare-blade silhouette to trace.
2. Blockout at real scale, one object per part.
3. Detail pass 1: refine the silhouette. HERO DETAIL = hineri-maki handle wrap — work out ONE
   crossing unit exactly like the refs, then array it. Work from hilt → blade.
4. Detail pass 2: add menuki, mekugi peg, kashira tie-off, kozuka, kurikata, sageo, tsuba hitsu-ana.
5. Detail pass 3: refine and clean.
6. UVs with no overlaps.
7. Texturing for wear and realism: patina and rust in crevices, rubbed edges, lacquer chips,
   hamon on the blade, braided cord.
8. Look-dev + renders: studio — hero shot + hilt, tip, tsuba, saya close-ups.
9. Output: .blend only.
Gates: pause after the blockout and after the first wrap unit.
Plan thoroughly first, then execute stage by stage.
```

## What each stage produced
| Stage | Result |
|---|---|
| 0 Plan | 4 questions asked: scope (saya: yes), wrap style (hineri-maki), use (high-detail render), refs (gather) |
| 1 References | 32 museum photos with licences logged; one koshirae shot from 7 angles chosen as the design set; a bare Bizen blade traced from pixels |
| 2 Blockout | blade + tang, habaki, seppa ×2, tsuba, fuchi, grip core, kashira, saya, at real scale |
| 3 Detail pass 1 | one 17 mm wrap unit (two cords, twisted crossings, paper hishigami) → Array ×10 + Lattice to the grip's hourglass + GN trim; then fittings refined hilt → blade; yokote crease and a smooth fukura tip |
| 4 Detail pass 2 | menuki with the cord bulging over them, mekugi through the real tang hole, kashira window + knot, ribbed saya, kozuka, kurikata, sageo, tsuba hitsu-ana |
| 5 Detail pass 3 | all hero parts watertight; blade checked to sit fully inside the saya |
| 6 UVs | cord UVs made at build time; the other parts packed in 4 sets; ≤ 5 overlapping px per set |
| 7 Texturing | 16 procedural materials; wear from AO and Pointiness; hamon from a blade attribute |
| 8 Look-dev | flat lay on a dark sweep, 3-point rig + reflection strip, 5 Cycles renders |

## Lessons that came out of it
All of them are in `skill/staged-3d-build/references/lessons.md`. The biggest:
- **Trace from pixels.** The eyeballed outline and ref anchor were both off by centimetres.
- **Repeated detail:** the wrap only looked right once it was modelled as one crossing unit, with the cord staying flat on the edges and diving into the crossing on each face.
- **Polished blade:** it needs a reflection card on the camera's mirror ray, or the hamon is invisible.
