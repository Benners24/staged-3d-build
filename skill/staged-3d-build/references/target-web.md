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
