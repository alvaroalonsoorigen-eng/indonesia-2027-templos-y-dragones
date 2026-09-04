import urllib.request, urllib.parse, json, time, os, sys
from PIL import Image, ImageDraw, ImageFont
import io, base64

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}

API_COMMONS = "https://commons.wikimedia.org/w/api.php"

# Map of images: (key, category, source_type, identifier_or_url, label)
# source_type: 'commons' (Wikimedia title) or 'direct' (URL)
PHOTOS = [
    # Destinos clave
    ("borobudur", "destino", "commons", "File:Borobudur Sunrise 2012-01-05.jpg", "Borobudur al amanecer (Java)"),
    ("prambanan", "destino", "commons", "File:Prambanan temple, Central Java, Indonesia, 20220818 1311 9139.jpg", "Templos de Prambanan (Java)"),
    ("padar", "destino", "commons", "File:Padar Island, Komodo National Park, Indonesia, 20250822 0911 2638.jpg", "Mirador de Isla Padar (Komodo)"),
    ("pink_beach", "destino", "commons", "File:Pink Beach, Padar Island, Komodo National Park, Indonesia, 20250822 1108 2678.jpg", "Pink Beach (Komodo)"),
    ("komodo_dragon", "destino", "commons", "File:Komodo dragon (Varanus komodoensis).jpg", "Dragón de Komodo en Rinca"),
    ("manta_ray", "destino", "commons", "File:Manta ray.jpg", "Mantarraya gigante en Manta Point"),
    ("turtle_siaba", "destino", "commons", "File:Total internal reflection of Chelonia mydas.jpg", "Tortuga marina en Siaba Besar"),
    ("kalong_sunset", "destino", "commons", "File:Flying fox at sunset 002.jpg", "Atardecer de zorros voladores en Kalong"),
    ("phinisi_boat", "destino", "commons", "File:Another boat waits near Pulau Kalong to see the bats (third stop) (16912463277).jpg", "Barco Phinisi tradicional en Komodo"),
    ("sidemen_rice", "destino", "commons", "File:RICE TERRACE OF SIDEMEN EAST BALI.jpg", "Terrazas de arroz del Valle de Sidemen"),
    ("pura_kehen", "destino", "commons", "File:Pura Kehen temple complex in Bali.jpg", "Templo ancestral Pura Kehen"),
    ("gunung_kawi", "destino", "commons", "File:Goddess of Rice, Dewi Sri, made from rice in a paddy field in Gunung Kawi 02.jpg", "Gunung Kawi y valles sagrados"),
    ("banyumala", "destino", "commons", "File:Banyumala Waterfall.jpg", "Cascadas gemelas de Banyumala (Munduk)"),
    ("tamblingan", "destino", "commons", "File:Lake Tamblingan.jpg", "Lago sagrado Tamblingan en canoa"),

    # 12 Alojamientos especiales
    ("hotel_taaktana", "hotel", "direct", "https://ak-d.tripcdn.com/images/0226z12000f5nvbpyA080_R_960_660_R5_D.jpg", "TA'AKTANA Luxury Collection (Labuan Bajo)"),
    ("hotel_ayana", "hotel", "direct", "https://luxecityguides.com/wp-content/uploads/2024/12/ayana-komodo-jetty.jpg", "AYANA Komodo Waecicu Beach (Espigón de 250m)"),
    ("hotel_sudamala", "hotel", "direct", "https://www.sudamalaresorts.com/app/uploads/2024/07/Hotel_SS_4-Photo-scaled.jpg", "Sudamala Resort Seraya (Isla privada y arrecife)"),
    ("hotel_plataran", "hotel", "direct", "https://balihospitalitygroup.com/wp-content/uploads/2015/02/BY9P1668.jpg", "Plataran Komodo Resort (Cala privada de Waecicu)"),
    ("hotel_lepirate", "hotel", "direct", "https://lepirate.com/wp-content/uploads/2023/02/LP-Island-Large.jpg", "Le Pirate Island (Pulau Sabolo glamping)"),
    ("hotel_menjangan_dynasty", "hotel", "direct", "https://penjorbalimandiri.com/wp-content/uploads/2016/12/Menjangan-Resort-view.jpg", "Menjangan Dynasty Resort (Safari y espigón)"),
    ("hotel_the_menjangan", "hotel", "direct", "https://www.trauminselreisen.de/fileadmin/_processed_/5/6/csm_19._Bali_Tower_-_Overview_9e4299ca6c.jpg", "The Menjangan (Bali Tower y parque nacional)"),
    ("hotel_bambu_indah", "hotel", "direct", "https://static.saltinourhair.com/wp-content/uploads/2023/04/28142651/bali-bamboo-hotels-Bambu-Indah-4-960x1440.jpg", "Bambu Indah Ubud (Arquitectura de bambú)"),
    ("hotel_camaya_hideout", "hotel", "direct", "https://static.designboom.com/wp-content/uploads/2020/06/hideout-horizon-bali-bamboo-studio-wna-designboom-1.jpg", "Hideout Bali / Camaya (Cabaña de bambú en río)"),
    ("hotel_munduk_moding", "hotel", "direct", "https://shewandersabroad.com/wp-content/uploads/2024/12/Infinity-pool-at-Munduk-Moding-Plantation-1-768x1152.jpg", "Munduk Moding Plantation (Piscina en las nubes)"),
    ("hotel_gili_asahan", "hotel", "direct", "https://natouralist.de/storage/lodges/gili-asahan-eco-lodge/37522/gili-asahan-eco-lodge.jpg", "Gili Asahan Eco Lodge (Playa virgen Secret Gilis)"),
    ("hotel_jeeva_beloam", "hotel", "direct", "https://www.greatsmallhotels.com/photos/92554_jeeva-beloam-beach-camp_.jpg", "Jeeva Beloam Beach Camp (Cala solitaria Sasak)")
]

def get_commons_url(file_title, width=1280):
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": str(width)
    }
    url = API_COMMONS + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "TripPlannerPersonal/1.0 (contacto en repo)"})
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode())
            pages = d.get("query", {}).get("pages", [])
            if pages and "imageinfo" in pages[0]:
                return pages[0]["imageinfo"][0].get("thumburl") or pages[0]["imageinfo"][0].get("url")
            return None
        except Exception as e:
            time.sleep(2 + intento * 2)
    return None

def fetch_and_crop(key, cat, stype, source, label, target_size=(800, 520), quality=76):
    webp_path = os.path.join(RAW_DIR, f"{key}.webp")
    if os.path.exists(webp_path) and os.path.getsize(webp_path) > 10000:
        print(f"[{key}] Already exists.")
        return webp_path

    if stype == "commons":
        url = get_commons_url(source)
    else:
        url = source

    if not url:
        print(f"[{key}] Error getting URL for {source}")
        return None

    print(f"[{key}] Downloading from {url[:70]}...")
    req = urllib.request.Request(url, headers=HEADERS)
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=35) as r:
                data = r.read()
            im = Image.open(io.BytesIO(data)).convert("RGB")
            
            # Crop to 800:520
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
            im.save(webp_path, "WEBP", quality=quality)
            print(f"[{key}] Saved {webp_path} ({os.path.getsize(webp_path)} bytes)")
            time.sleep(0.5)
            return webp_path
        except Exception as e:
            print(f"[{key}] Attempt {intento+1} failed: {e}")
            time.sleep(2 + intento * 2)
    return None

print("=== INICIANDO DESCARGA Y PROCESAMIENTO DE FOTOS ===")
cache = {}
saved_paths = []

for key, cat, stype, source, label in PHOTOS:
    p = fetch_and_crop(key, cat, stype, source, label)
    if p and os.path.exists(p):
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        cache[key] = {
            "label": label,
            "cat": cat,
            "b64": f"data:image/webp;base64,{b64}"
        }
        saved_paths.append((key, p, label))
    else:
        print(f"CRITICAL: Failed {key}")

# Save imgcache.json
cache_file = os.path.join(BASE, "imgcache.json")
with open(cache_file, "w") as f:
    json.dump(cache, f)

print(f"\nGenerado imgcache.json con {len(cache)} fotos ({os.path.getsize(cache_file)/1024/1024:.2f} MB)")

# Create Contact Sheet (Hoja de contactos)
print("Generando hoja de contactos...")
cols = 4
rows = (len(saved_paths) + cols - 1) // cols
cw, ch = 320, 208
sheet = Image.new("RGB", (cols * cw, rows * ch), (20, 24, 30))
draw = ImageDraw.Draw(sheet)

for idx, (key, path, label) in enumerate(saved_paths):
    r = idx // cols
    c = idx % cols
    im = Image.open(path).resize((cw - 8, ch - 24), Image.Resampling.LANCZOS)
    sheet.paste(im, (c * cw + 4, r * ch + 4))
    draw.text((c * cw + 6, r * ch + ch - 18), f"{key}: {label[:26]}", fill=(240, 240, 240))

sheet_path = os.path.join(BASE, "hoja_contactos.jpg")
sheet.save(sheet_path, "JPEG", quality=85)
print(f"Hoja de contactos guardada en {sheet_path}")
