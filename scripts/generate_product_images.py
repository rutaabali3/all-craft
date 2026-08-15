from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
import json
import time
import requests

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "image_manifest.tsv"
LOG = ROOT / "pixelster_generation_log.jsonl"
API = "https://ahm7xmakki.com/api/tti"

session = requests.Session()


def generate(row):
    target = ROOT / row["image_path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {"prompt": row["prompt"], "ratio": "1:1"}
    last_error = None
    for attempt in range(1, 4):
        try:
            response = session.post(API, json=payload, timeout=150)
            response.raise_for_status()
            data = response.json()
            image_url = data.get("imageUrl")
            if not image_url:
                raise RuntimeError(f"missing imageUrl: {data}")
            image = session.get(image_url, timeout=150)
            image.raise_for_status()
            if len(image.content) < 10_000:
                raise RuntimeError(f"image too small: {len(image.content)} bytes")
            target.write_bytes(image.content)
            return {"slug": row["slug"], "status": "generated", "path": str(target), "bytes": len(image.content), "imageUrl": image_url}
        except Exception as exc:
            last_error = repr(exc)
            time.sleep(2 * attempt)
    return {"slug": row["slug"], "status": "failed", "error": last_error, "path": str(target)}


with MANIFEST.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

results = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(generate, row) for row in rows]
    for index, future in enumerate(as_completed(futures), start=1):
        result = future.result()
        results.append(result)
        print(f"[{index}/{len(rows)}] {result['slug']}: {result['status']}", flush=True)

results.sort(key=lambda item: item["slug"])
with LOG.open("w", encoding="utf-8") as handle:
    for result in results:
        handle.write(json.dumps(result, ensure_ascii=False) + "\n")

failed = [result for result in results if result["status"] == "failed"]
print(f"completed={len(results)} failed={len(failed)} log={LOG}")
if failed:
    print("failed slugs:", ", ".join(result["slug"] for result in failed))
    raise SystemExit(1)
