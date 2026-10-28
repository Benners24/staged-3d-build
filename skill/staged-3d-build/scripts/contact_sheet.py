"""Tile every image in a folder into one labelled contact sheet (needs Pillow).

  python -I contact_sheet.py refs                    # -> refs/_contact_sheet.jpg
  python -I contact_sheet.py refs --pattern "full_*" --out _full.jpg --cell 400
"""
import argparse, glob, os
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("folder")
ap.add_argument("--pattern", default="*.jpg")
ap.add_argument("--out", default="_contact_sheet.jpg")
ap.add_argument("--cell", type=int, default=320)
ap.add_argument("--cols", type=int, default=5)
a = ap.parse_args()

files = [f for f in sorted(glob.glob(os.path.join(a.folder, a.pattern))) if not os.path.basename(f).startswith("_")]
if not files:
    raise SystemExit("no images match")
rows = (len(files) + a.cols - 1) // a.cols
sheet = Image.new("RGB", (a.cols * a.cell, rows * (a.cell + 20)), "white")
draw = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB")
    im.thumbnail((a.cell - 6, a.cell - 6))
    x, y = (i % a.cols) * a.cell, (i // a.cols) * (a.cell + 20)
    sheet.paste(im, (x + (a.cell - im.width) // 2, y + (a.cell - im.height) // 2))
    draw.text((x + 4, y + a.cell + 3), os.path.basename(f)[:44], fill="black")
out = os.path.join(a.folder, a.out)
sheet.save(out, quality=85)
print(len(files), "images ->", out)
