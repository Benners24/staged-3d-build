# Staged 3D Build

A template for building **props, weapons, characters and Roblox avatar/UGC items** in Blender with
Claude Code. Claude plans the build thoroughly, then runs it **stage by stage**, checking each stage
against the references before the next one starts.

It packages two things:
- **A fill-in prompt** ([`PROMPT_TEMPLATE.md`](skill/staged-3d-build/PROMPT_TEMPLATE.md)) you paste into Claude Code.
- **A Claude Code skill** ([`skill/staged-3d-build`](skill/staged-3d-build)) that knows the stages, the checks and the pitfalls, and ships helper scripts.

```
 0 Plan ─► 1 References ─► 2 Blockout ─► 3 Detail pass 1 ─► 4 Detail pass 2 ─► 5 Detail pass 3
 (plan      every angle,     real scale,    silhouette +       add secondary      refine + clean
  mode)     trace source     one obj/part   ONE hero unit      details            (0 open edges)
                             [pause]        → array  [pause]
         ─► 6 UVs ─► 7 Texturing ─► 8 Look-dev ─► 9 Output
            0 overlap   wear where      lights,       .blend / baked GLB /
            (raster)    physics puts it renders       Roblox checks
```

## Why stages
- **Wrong proportions get caught early.** Each stage has one deliverable and one check, so a mistake shows up at the blockout, not after texturing.
- **The repeated detail is built once.** A wrap, braid, chain or row of plates is modelled as **one unit**, reviewed, then arrayed and fitted to the shape. One long procedural shape never centres right.
- **Every part comes from a re-runnable script.** Any stage can be redone without breaking the ones after it.

## Requirements
- Blender 4.2+ (tested on 5.2) with an MCP bridge, e.g. [MCP for Blender](https://mcp-for-blender.com).
- Claude Code.
- Python 3 with Pillow, for the reference scripts.

## Install the skill
```bash
git clone https://github.com/Benners24/staged-3d-build.git
# macOS / Linux
cp -r staged-3d-build/skill/staged-3d-build ~/.claude/skills/
# Windows (PowerShell)
Copy-Item -Recurse staged-3d-build\skill\staged-3d-build $env:USERPROFILE\.claude\skills\
```
Restart Claude Code. The skill triggers on requests such as "make a medieval lantern prop in Blender", or you can call it directly with `/staged-3d-build`.

## Use the prompt
1. Open [`PROMPT_TEMPLATE.md`](skill/staged-3d-build/PROMPT_TEMPLATE.md).
2. Copy the block and fill in the `[...]` fields. The important ones:
   - **HERO DETAIL:** the repeated element;
   - **direction:** e.g. hilt → blade;
   - **wear notes;**
   - **gates:** pause, or run straight through.
3. Paste it into Claude Code. Claude asks only the questions that change the work, writes a plan for you to approve, then executes.

See [`templates/examples/wakizashi.md`](templates/examples/wakizashi.md) for a real run: the one-line request it came from, the filled template, and what each stage produced.

## What's in the skill
| File | Purpose |
|---|---|
| `SKILL.md` | the orchestrator: stage table, gates, working rules |
| `references/stages.md` | the playbook for each stage (goal, steps, deliverables, verify, gate) |
| `references/target-*.md` | specifics for props, characters, Roblox, and web/GLB output |
| `references/lessons.md` | pitfalls and fixes learned in real builds |
| `scripts/fetch_refs.py` | Wikimedia Commons reference download with licence log (`SOURCES.md`) |
| `scripts/contact_sheet.py` | labelled contact sheet of a reference folder |
| `scripts/trace_silhouette.py` | pixel-accurate outline trace → JSON in metres + debug overlay |
| `scripts/bl_lib.py` | Blender helpers: lofts, rings, image refs at real scale, booleans, freezing arrays |
| `scripts/bl_cleanup.py` | mesh hygiene + open-edge report |
| `scripts/bl_uv_overlap_check.py` | raster UV-overlap check per texture set |
| `scripts/bl_lookdev_studio.py` | studio lights, reflection card, backdrop, cameras, Cycles GPU |

## Companion skills (optional)
If installed, the skill hands off to `blender-reference-model` (single-image tracing),
`blender-look-dev`, `blender-web-export`, `roblox-character-blender`, and a vault checkpoint skill.
It works without them.

## Reference images
No reference images are included. `fetch_refs.py` records each image's licence and author, so
respect them: CC BY / BY-SA need attribution, and museum CC0 / public-domain images are free to use.

## Credits
Made by **Benners24** in collaboration with **TheBonfiree**, built with Claude Code.
Licensed under MIT; see [LICENSE](LICENSE).
