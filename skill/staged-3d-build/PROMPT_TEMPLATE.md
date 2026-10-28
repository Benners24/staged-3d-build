# Staged 3D Build — prompt template

Copy everything inside the box, replace each `[...]`, and send it. Delete any line that doesn't apply.
Words in CAPS are the parts that most change the result.

```
Build a [TYPE: prop | weapon | character | creature | Roblox avatar/UGC item] — [OBJECT]
([style / era / franchise / material notes]).

Use: [high-detail render | web GLB under N triangles | Roblox spec | game asset]
Include: [main parts + extras, e.g. "sword + scabbard"]   Exclude: [things to leave out]
References: [gather public-domain/CC refs | use mine at PATH]
  — every angle (front, back, sides, top/bottom) + close-ups of [the details that matter].
Real size: [known dimensions | derive from refs].

Stages:
1. References for each angle → pick ONE design set + a clean silhouette to trace.
2. Blockout at real scale, one object per part.
3. Detail pass 1: refine the silhouette. HERO DETAIL = [the repeated element, e.g. handle wrap,
   braid, chain link, armor plate, stitch row] — work out ONE unit exactly like the refs,
   then array/repeat it. Work from [A] to [B] (e.g. hilt → blade, head → feet, core → edges).
4. Detail pass 2: add [secondary details, e.g. rivets, engravings, buckles, seams].
5. Detail pass 3: refine and clean (topology, fits, smoothing, naming).
6. UVs with no overlaps.
7. Texturing for wear and realism: [rust, chips, dirt in crevices, rubbed edges, fabric weave,
   faded paint, scratches...].
8. Look-dev + renders: [studio | dramatic | outdoor] — [hero shot + close-ups of ...].
9. Output: [.blend only | baked GLB for web | Roblox export].

Gates: [pause after the blockout and after the first hero unit | run straight through after
I approve the plan].
Plan thoroughly first, then execute stage by stage.
```

## Filled example (one line → full template)
Original request:
> test build make a Wakizashi. Look up references for each angles. Once you gathered reference
> proceed with the blocking of the shape then add the first out of 3 detail pass. 1st is refine
> the silhoette the wrappping of the handle has to be precise like how they wrapped it, work out
> the first wrap then array it, then moving from the hilt to the blade. The rest of the detail
> pass is just furthur to add, refine, and clean details. Next is texturing for some wear and realism

| Field | Filled |
|---|---|
| TYPE / OBJECT | weapon, wakizashi (Edo-period short sword) |
| Use | high-detail render |
| Include | sword + saya (scabbard) |
| References | gather public-domain/CC museum photos, every angle + wrap, tsuba, kissaki close-ups |
| HERO DETAIL | hineri-maki tsuka-ito: one crossing unit, then arrayed; hilt → blade |
| Pass 2 | menuki, mekugi, kashira tie-off, kozuka, kurikata, sageo, tsuba hitsu-ana |
| Wear | AO dirt/patina, rubbed edges, rust in iron pits, lacquer chips, hamon |
| Gates | pause after blockout + hero unit, then run through |
