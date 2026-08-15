from pathlib import Path
from bs4 import BeautifulSoup
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
OUT = ROOT / "unique_image_manifest.tsv"


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def product_name(soup, slug):
    title = clean(soup.title.get_text(" ", strip=True) if soup.title else slug)
    return clean(title.split(" - Premium ", 1)[-1] if " - Premium " in title else slug.replace("-craft", "").replace("-", " "))

rows = []
for directory in sorted(p for p in PROJECTS.iterdir() if p.is_dir()):
    html_path = directory / "index.html"
    if not html_path.exists():
        continue
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    product = product_name(soup, directory.name)
    images = soup.select('img[src="./image/item.png"]')
    for index, image in enumerate(images, start=1):
        classes = set(image.get("class", []))
        role = "product variation" if "type-img" in classes else ("hero presentation" if "hero-img" in classes else "about presentation")
        card = image.find_parent(class_="type-card")
        heading = clean(card.find("h4").get_text(" ", strip=True)) if card and card.find("h4") else ""
        description = clean(card.find("p").get_text(" ", strip=True)) if card and card.find("p") else ""
        features = " ".join(clean(li.get_text(" ", strip=True)) for li in card.select(".type-features li")) if card else ""
        variation = heading or f"{role} {index}"
        if role == "product variation":
            prompt = (
                f"A distinct premium catalog photograph of {product}, variation {index}: {variation}. "
                f"Show the real {product} object clearly and accurately, with a different physical presentation from every other asset: {description} "
                f"Product details: {features}. Use a distinct angle, arrangement, and tasteful material/color variation while keeping the item recognizable. "
                "Single product focus, realistic proportions, soft studio lighting, warm off-white craft-paper background, "
                "subtle natural shadow, no text, no logos, no watermark, square composition."
            )
        else:
            prompt = (
                f"A distinct editorial presentation image for a stationery and craft product webpage about {product}, "
                f"role {role} number {index}. Feature {product} as the clear subject in a unique composition, "
                "different from every other image in the repository, realistic product photography, soft studio lighting, "
                "warm off-white craft-paper background, no text, no logos, no watermark, square composition."
            )
        filename = f"unique-{index:02d}.png" if len(images) < 100 else f"unique-{index:03d}.png"
        rows.append({
            "slug": directory.name,
            "index": index,
            "role": role,
            "product": product,
            "variation": variation,
            "description": description,
            "features": features,
            "prompt": prompt,
            "image_path": f"projects/{directory.name}/image/{filename}",
            "old_src": "./image/item.png",
            "new_src": f"./image/{filename}",
        })

with OUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote {len(rows)} unique image slots to {OUT}")
