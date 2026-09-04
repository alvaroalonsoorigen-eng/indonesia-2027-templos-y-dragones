import urllib.request, urllib.parse, json, os, time
from PIL import Image
import io, base64

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE, "raw")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

def save_cropped(data, key, target_size=(900, 580), quality=82):
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
    out_path = os.path.join(RAW_DIR, f"{key}.webp")
    im.save(out_path, "WEBP", quality=quality)
    print(f"Saved {key}.webp: {os.path.getsize(out_path)/1024:.1f} KB")

# 1. Phinisi Boat: Sailing Phinisi in Komodo National Park
print("1. Phinisi boat...")
u_phinisi = "https://www.komodoluxury.com/wp-content/uploads/2026/03/Sailing-Phinisi-in-Komodo-National-Park.webp"
try:
    req = urllib.request.Request(u_phinisi, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        save_cropped(r.read(), "phinisi_boat")
except Exception as e:
    print("Phinisi error:", e)

# 2. Kalong Island sunset from Commons:
print("2. Kalong Island sunset...")
u_kalong_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&titles=File:Dusk%20%26%20Dawn%20in%20Kalong%20Island,%20Labuan%20Bajo.jpg&prop=imageinfo&iiprop=url&iiurlwidth=1280"
try:
    req = urllib.request.Request(u_kalong_api, headers={"User-Agent": "TripPlanner/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read().decode())
    pages = d["query"]["pages"]
    thumb = list(pages.values())[0]["imageinfo"][0]["thumburl"]
    req2 = urllib.request.Request(thumb, headers={"User-Agent": "TripPlanner/1.0"})
    with urllib.request.urlopen(req2, timeout=15) as r2:
        save_cropped(r2.read(), "kalong_sunset")
except Exception as e:
    print("Kalong error:", e)

# 3. Borobudur golden stupas from Commons:
print("3. Borobudur stupas...")
u_boro_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&titles=File:Borobudur-Temple-Park%20Indonesia%20Stupas-of-Borobudur-04.jpg&prop=imageinfo&iiprop=url&iiurlwidth=1280"
try:
    req = urllib.request.Request(u_boro_api, headers={"User-Agent": "TripPlanner/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read().decode())
    pages = d["query"]["pages"]
    thumb = list(pages.values())[0]["imageinfo"][0]["thumburl"]
    req2 = urllib.request.Request(thumb, headers={"User-Agent": "TripPlanner/1.0"})
    with urllib.request.urlopen(req2, timeout=15) as r2:
        save_cropped(r2.read(), "borobudur")
except Exception as e:
    print("Borobudur error:", e)

# 4. Sebayur Island / Komodo Resort:
print("4. Komodo Resort Sebayur...")
u_sebayur = "https://almiratrip.com/wp-content/uploads/2024/04/Sebayur-Island-Labuan-Bajo-scaled.jpg"
try:
    req = urllib.request.Request(u_sebayur, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        save_cropped(r.read(), "hotel_komodo_resort")
except Exception as e:
    print("Sebayur error:", e)

# 5. Plataran Komodo:
print("5. Plataran Komodo...")
u_plataran = "https://luxeindonesiatravel.com/wp-content/uploads/2023/05/hotel-platarankomodoflores-03-1024x683-1.jpg"
try:
    req = urllib.request.Request(u_plataran, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        save_cropped(r.read(), "hotel_plataran")
except Exception as e:
    print("Plataran error:", e)

print("Upgrade complete!")
