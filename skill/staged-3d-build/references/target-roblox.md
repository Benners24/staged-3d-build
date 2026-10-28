# Target: Roblox avatar / UGC

Use the same stages, with the specs as hard limits checked at blockout, pass 3 and output.

- **If `roblox-character-blender` is installed:** follow its type selection (R15 body, layered clothing, rigid accessory, dynamic head) and its spec file for the numbers (`roblox-character-blender/references/roblox-avatar-specs.md`, in the same skills folder as this skill). If `roblox-avatar-designer` is installed, use it for classic 2D clothing templates.
- **Otherwise:** take every number from the official docs at https://create.roblox.com/docs/art/characters (body/accessory/clothing specification pages). Never guess. Any number you couldn't verify gets marked UNVERIFIED in the plan.

## Say these up front (before any work)
- **The user does the upload.** Importing in Studio, the Accessory Fitting Tool, the creator fee and Roblox moderation review happen outside Blender and can take longer than the build. Never promise "live today".
- **Quick requests:** use the Quick path in SKILL.md; the spec limits below are never skipped.

## Spec numbers and unknowns
- Take every limit from `roblox-avatar-specs.md` (or the official docs). It records triangle limits (e.g. 4k for a hat), the 2048×2048 texture cap, and bounding boxes in studs per accessory type.
- **Not verified in the spec file:** the stud-to-Blender-unit (or metre) conversion and the best Blender scene unit scale. Use the official Roblox Blender template files for scale instead of guessing, and check the bounding box against the spec box before and after export.
- **Bounding box first:** at the blockout, compare the whole piece to the accessory box. A wide brim, cape or wing breaks the box long before the triangle limit, so decide the size at the blockout, not at the end.

## Triangle budget with a repeated detail
Arrays multiply triangles. Before building the hero unit, write the budget down: total limit, an allowance for the repeated detail, and the allowance for everything else. Then count: unit triangles × copies. A common split to start from is about a third for the hero detail; adjust it if the detail is the whole point of the item.

## Baking for Roblox
Roblox uses image textures, so procedural wear is baked (`target-web.md`, steps 2–3) into one set up to 2048×2048. The spec file says textures are applied with a SurfaceAppearance or TextureID but does not list which PBR maps are supported: mark that UNVERIFIED in the plan and check the live docs before baking more than base colour.

## Stage notes
- **Blockout:** build to the official R15 proportions and attachment points of the chosen avatar type. Units: Roblox studs ↔ metres as in the spec.
- **Pass 1 hero detail:** repeated accessory elements (chain links, plates, braids) still use one unit + array. Watch the triangle budget, because arrays multiply it.
- **Pass 3:** apply all modifiers; triangle count within the budget; names and attachments as the spec requires; no n-gons; scale applied.
- **UVs/texturing:** keep within the texture size limit. Bake procedural wear into an image (see `target-web.md`) because Roblox uses image textures.
- **Output:** FBX/OBJ export per the spec, and only when asked. Otherwise stop at the saved `.blend`.
