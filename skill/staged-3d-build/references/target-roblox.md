# Target: Roblox avatar / UGC

Use the same stages, with the specs as hard limits checked at blockout, pass 3 and output.

- **If `roblox-character-blender` is installed:** follow its type selection (R15 body, layered clothing, rigid accessory, dynamic head) and its spec reference for the numbers. If `roblox-avatar-designer` is installed, use it for classic 2D clothing templates.
- **Otherwise:** take every number from the official docs at https://create.roblox.com/docs/art/characters (body/accessory/clothing specification pages). Never guess. Any number you couldn't verify gets marked UNVERIFIED in the plan.

## Stage notes
- **Blockout:** build to the official R15 proportions and attachment points of the chosen avatar type. Units: Roblox studs ↔ metres as in the spec.
- **Pass 1 hero detail:** repeated accessory elements (chain links, plates, braids) still use one unit + array. Watch the triangle budget, because arrays multiply it.
- **Pass 3:** apply all modifiers; triangle count within the budget; names and attachments as the spec requires; no n-gons; scale applied.
- **UVs/texturing:** keep within the texture size limit. Bake procedural wear into an image (see `target-web.md`) because Roblox uses image textures.
- **Output:** FBX/OBJ export per the spec, and only when asked. Otherwise stop at the saved `.blend`.
