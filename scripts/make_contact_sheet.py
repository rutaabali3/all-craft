from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "image_manifest.tsv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

indices = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 162]
thumb_w, thumb_h = 260, 300
cols = 3
rows_count = math.ceil(len(indices) / cols)
out = Image.new("RGB", (cols * thumb_w, rows_count * thumb_h), "#f4efe7")
draw = ImageDraw.Draw(out)
for pos, idx in enumerate(indices):
    row = rows[idx]
    image = Image.open(ROOT / row["image_path"]).convert("RGB")
    image.thumbnail((240, 240))
    x = (pos % cols) * thumb_w + 10
    y = (pos // cols) * thumb_h + 10
    out.paste(image, (x + (240-image.width)//2, y))
    label = row["product"][:34]
    draw.text((x, y + 245), label, fill="#241f1a")
    draw.text((x, y + 265), row["slug"][:34], fill="#665b50")
out.save(ROOT / "pixelster_contact_sheet.jpg", quality=92)
print(out.size)
