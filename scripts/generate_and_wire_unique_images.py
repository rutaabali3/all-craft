from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import json
import time
import requests

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "unique_image_manifest.tsv"
LOG = ROOT / "unique_pixelster_generation_log.jsonl"
API = "https://ahm7xmakki.com/api/tti"


def validate_slug(slug: str) -> str:
    """Validate that slug is a simple directory name without path traversal sequences."""
    if not slug or not isinstance(slug, str):
        raise ValueError(f"Invalid slug: {slug!r}")
    if "/" in slug or "\\" in slug or "\0" in slug:
        raise ValueError(f"Slug contains path separators or invalid characters: {slug!r}")
    if slug in (".", ".."):
        raise ValueError(f"Slug cannot be '.' or '..': {slug!r}")
    p = Path(slug)
    if p.is_absolute() or p.name != slug:
        raise ValueError(f"Slug must be a simple directory name: {slug!r}")
    projects_dir = (ROOT / "projects").resolve()
    target_dir = (projects_dir / slug).resolve()
    if target_dir.parent != projects_dir:
        raise ValueError(f"Slug path traversal detected: {slug!r}")
    return slug


def generate(row):
    slug = validate_slug(row["slug"])
    target = (ROOT / row["image_path"]).resolve()
    projects_dir = (ROOT / "projects").resolve()
    if not target.is_relative_to(projects_dir):
        raise ValueError(f"Invalid image_path outside projects directory: {row['image_path']!r}")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {"prompt": row["prompt"], "ratio": "1:1"}
    last_error = None
    for attempt in range(1, 4):
        try:
            response = requests.post(API, json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()
            image_url = data.get("imageUrl")
            if not image_url:
                raise RuntimeError(f"missing imageUrl: {data}")
            image = requests.get(image_url, timeout=180)
            image.raise_for_status()
            if len(image.content) < 10_000:
                raise RuntimeError(f"image too small: {len(image.content)} bytes")
            target.write_bytes(image.content)
            return {"slug": slug, "index": int(row["index"]), "status": "generated", "path": str(target), "bytes": len(image.content), "imageUrl": image_url}
        except Exception as exc:
            last_error = repr(exc)
            time.sleep(2 * attempt)
    return {"slug": slug, "index": int(row["index"]), "status": "failed", "error": last_error, "path": str(target)}


def main():
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    results = []
    with ThreadPoolExecutor(max_workers=24) as executor:
        futures = [executor.submit(generate, row) for row in rows]
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            print(f"[{index}/{len(rows)}] {result['slug']} #{result['index']}: {result['status']}", flush=True)

    results.sort(key=lambda item: (item["slug"], item["index"]))
    with LOG.open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")

    failed = [result for result in results if result["status"] == "failed"]
    if failed:
        print(f"completed={len(results)} failed={len(failed)} log={LOG}")
        raise SystemExit(1)

    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        manifest_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in manifest_rows:
        slug = validate_slug(row["slug"])
        projects_dir = (ROOT / "projects").resolve()
        html_path = (projects_dir / slug / "index.html").resolve()
        if not html_path.is_relative_to(projects_dir):
            raise ValueError(f"Invalid slug path traversal: {slug!r}")
        text = html_path.read_text(encoding="utf-8")
        old = 'src="./image/item.png"'
        new = f'src="{row["new_src"]}"'
        if old not in text:
            raise RuntimeError(f"missing source reference for {slug} #{row['index']}")
        text = text.replace(old, new, 1)
        html_path.write_text(text, encoding="utf-8")

    print(f"completed={len(results)} failed=0 log={LOG}")
    print(f"rewired={len(manifest_rows)} html image references")


if __name__ == "__main__":
    main()
