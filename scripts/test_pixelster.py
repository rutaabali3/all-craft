import json
import requests

payload = {
    "prompt": "A clean premium product catalog photograph of acrylic paint tubes, the actual objects clearly visible and centered, realistic materials and proportions, soft studio lighting, warm off-white craft-paper background, subtle shadow, no text, no logos, no watermark, square composition",
    "ratio": "1:1",
}
response = requests.post("https://ahm7xmakki.com/api/tti", json=payload, timeout=120)
print("status", response.status_code)
print("content-type", response.headers.get("content-type"))
print(response.text[:4000])
