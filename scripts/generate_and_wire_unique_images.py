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


def generate(row):
    target = ROOT / row["image_path"]
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
            with requests.get(image_url, stream=True, timeout=180) as image:
                image.raise_for_status()
                bytes_downloaded = 0
                try:
                    with target.open("wb") as f:
                        for chunk in image.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                bytes_downloaded += len(chunk)
                    if bytes_downloaded < 10_000:
                        raise RuntimeError(f"image too small: {bytes_downloaded} bytes")
                except Exception:
                    if target.exists():
                        target.unlink()
                    raise
            return {"slug": row["slug"], "index": int(row["index"]), "status": "generated", "path": str(target), "bytes": bytes_downloaded, "imageUrl": image_url}
        except Exception as exc:
            last_error = repr(exc)
            time.sleep(2 * attempt)
    return {"slug": row["slug"], "index": int(row["index"]), "status": "failed", "error": last_error, "path": str(target)}


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
        html_path = ROOT / "projects" / row["slug"] / "index.html"
        text = html_path.read_text(encoding="utf-8")
        old = 'src="./image/item.png"'
        new = f'src="{row["new_src"]}"'
        if old not in text:
            raise RuntimeError(f"missing source reference for {row['slug']} #{row['index']}")
        text = text.replace(old, new, 1)
        html_path.write_text(text, encoding="utf-8")

    print(f"completed={len(results)} failed=0 log={LOG}")
    print(f"rewired={len(manifest_rows)} html image references")


if __name__ == "__main__":
    main()
