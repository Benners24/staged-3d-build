# Target: props and weapons (hard surface)

## Reference checklist
- **Square-on profile**, plain background, for tracing. Museum "object photography" is ideal.
- **Thickness views:** top/spine and bottom/edge views give the cross-section.
- **Close-ups** of every joint/fitting, every repeated element (wrap, rivets, chain), and the ends (tips, caps, pommels).
- **A scale cue** (ruler, known part) in at least one photo.

## Modelling recipes
- **Profile lofts:** trace top and bottom edges per column (`trace_silhouette.py`), then build stations along the long axis. Each station is a ring that encodes the real cross-section: ridge lines, bevels, convex "niku". Mark ridge lines sharp along the length.
- **Ends and tips:**
  - traces get noisy in the last few px;
  - replace with a cubic Hermite from the traced width to 0;
  - match the traced slope at the join, so there's no kink.
- **Facets** (e.g. a tip facet): change the section parameters by a few % past the line and mark that ring sharp. That gives a crisp crease without extra geometry.
- **Fittings** (guards, collars, caps, ferrules): rings offset from the host section plus a margin. Neighbours overlap about 1 mm. Make the margin cover any raised detail that tucks under them.
- **Plates and discs:** lathe a radial profile (rim, plate, bevel). Use smooth by angle so the flat caps don't streak.
- **Holes, windows, pockets:** boolean the cutters, then apply them. Line up the parts that pass through holes, using the same constants in both scripts.
- **Containers** (scabbards, sheaths, holsters): follow a smooth fit of the contained part's long curve, not its tip kink. Check numerically that every vertex of the contained part is inside.

## Typical hero details
Grip wraps, cord or leather bindings, chain mail rows, rivet lines, scale or lamellar plates, stitched seams. Build one period, then use Array + Lattice.

## Typical wear
| Material | Wear and finish |
|---|---|
| Iron | rust in pits (AO × noise); rubbed edges lighter and smoother |
| Brass / copper / gold | dark patina in recesses; polished high points |
| Lacquer / paint | chips at the ends and edges (pointiness × noise × end mask); clear coat micro-scratches |
| Polished steel | lengthwise polish scratches; faint grain; heat-treatment patterns from attributes |
