import urllib.request, urllib.parse, json, os, re
from PIL import Image
import io

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

def download_and_crop(url, out_name, target_size=(900, 580), quality=84, extra_headers=None):
    h = dict(HEADERS)
    if extra_headers:
        h.update(extra_headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        im = Image.open(io.BytesIO(data)).convert("RGB")
        tw, th = target_size
        target_ratio = tw / th
        w, h = im.size
        current_ratio = w / h
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            im = im.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            im = im.crop((0, top, w, top + new_h))
        im = im.resize(target_size, Image.Resampling.LANCZOS)
        out_path = os.path.join("raw", out_name)
        im.save(out_path, "WEBP", quality=quality)
        print(f"OK {out_name}: {os.path.getsize(out_path)/1024:.1f} KB")
        return True
    except Exception as e:
        print(f"FAIL {out_name}: {e}")
        return False

# Search and test high-res candidates for Phinisi, Kalong, Komodo Resort, Borobudur, Taaktana
print("Testing upgrades...")
# 1. Phinisi Boat: high-res, majestic sailing schooner in Komodo
download_and_crop(
    "https://upload.wikimedia.org/wikipedia/commons/e/ea/Phinisi_boat_in_Komodo_National_Park.jpg",
    "phinisi_boat.webp"
)

# 2. Kalong sunset: gorgeous dramatic sunset over the islands with flying foxes
download_and_crop(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Sunset_at_Kalong_Island%2C_Komodo_National_Park.jpg/1280px-Sunset_at_Kalong_Island%2C_Komodo_National_Park.jpg",
    "kalong_sunset.webp"
)

# 3. Borobudur golden morning:
download_and_crop(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Borobudur-Nirvana-Sunrise.jpg/1280px-Borobudur-Nirvana-Sunrise.jpg",
    "borobudur.webp"
)
