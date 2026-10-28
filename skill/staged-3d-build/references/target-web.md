# Target: web / GLB output

Procedural Cycles materials (AO, Pointiness, noise) and lights do **not** export to glTF. Bake first.

1. **Budget:** pick a triangle budget (typical hero prop: 30–80k tris) and a texture size (2K per set). Decimate or re-loft any part over budget. Arrays: apply them, then decimate the unit before arraying if possible.
2. **Bake set-up:**
   - make a duplicate scene or file for baking, so the render file stays intact;
   - per texture set, create a new image (2048², non-colour for the data maps);
   - add an Image Texture node (not connected) to every material in the set and make it active.
3. **Bake** (Cycles):
   - Diffuse colour only → `<set>_basecolor.png`;
   - Roughness → `<set>_roughness.png`;
   - Normal (tangent) → `<set>_normal.png`, from the bump chains;
   - metallic: bake through an Emission swap of the metallic value, or set it per material if it is uniform;
   - margin 8 px.
4. **Rebuild** simple Principled materials from the baked maps. Check in Material Preview that they match the procedural renders.
5. **Export** with `blender-web-export` if installed (compressed GLB + viewer page). Otherwise: File › Export › glTF 2.0, apply modifiers, +Y up, Draco compression.
6. **Verify:**
   - file size;
   - triangle count;
   - open it in a glTF viewer (or the generated page);
   - textures aren't stretched;
   - normals face the right way.

## Glow / emission (energy cells, lamps, screens)
- A glow is an emissive texture plus an emission strength; the bloom around it is added by the viewer, not baked.
- Bake: give the glowing material its colour as Emission, set other materials' emission to black, then bake the **Emit** pass to `<set>_emissive.png`.
- In the rebuilt Principled material: plug that image into Emission Color and set Emission Strength (glTF carries it; strengths above 1 need the emissive-strength extension that Blender's glTF exporter writes).
- Verify in the viewer that bloom is enabled; if not, the cells will look flat. Flag it to the user.

## Triangle budget starting points (check against the page's real needs; ask when unsure)
| Object | Starting budget |
|---|---|
| small handheld prop (pistol, lantern, tool) | 5–20k tris |
| large hero prop or vehicle | 20–50k tris |
| character | 20–60k tris |
Use the low end when the page also loads a lot else, or the user says "light". Count tris per part at every stage, not only at export, and texture fine detail rather than modelling it.
