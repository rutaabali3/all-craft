from pathlib import Path
from bs4 import BeautifulSoup
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
OUT = ROOT / "image_manifest.tsv"


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()

rows = []
for directory in sorted(p for p in PROJECTS.iterdir() if p.is_dir()):
    html_path = directory / "index.html"
    if not html_path.exists():
        continue
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    title = clean(soup.title.get_text(" ", strip=True) if soup.title else directory.name)
    h1 = clean(soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else title)
    product = title.split(" - Premium ", 1)[-1].strip() if " - Premium " in title else directory.name.replace("-craft", "").replace("-", " ")
    product = clean(product)
    prompt = (
        f"A clean premium product catalog photograph of {product}, the actual object clearly visible and centered, "
        "single item or small natural set, realistic materials and proportions, soft studio lighting, "
        "warm off-white craft-paper background, subtle shadow, no text, no logos, no watermark, square composition"
    )
    rows.append({"slug": directory.name, "title": title, "heading": h1, "product": product, "prompt": prompt, "image_path": f"projects/{directory.name}/image/item.png"})

with OUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote {len(rows)} rows to {OUT}")
