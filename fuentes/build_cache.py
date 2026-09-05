import os, json, base64
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE, "raw")

ITEMS = [
    # 14 Destinos / Experiencias
    ("borobudur", "Borobudur al amanecer (Java)", "destino"),
    ("prambanan", "Prambanan, templo hinduista (Java)", "destino"),
    ("padar", "Isla Padar, mirador 3 bahías (Komodo)", "destino"),
    ("pink_beach", "Pink Beach, arena rosa y arrecife (Komodo)", "destino"),
    ("komodo_dragon", "Dragón de Komodo en su hábitat (Rinca)", "destino"),
    ("manta_ray", "Mantarraya gigante (Manta Point)", "destino"),
    ("turtle_siaba", "Tortuga marina en Siaba Besar", "destino"),
    ("kalong_sunset", "Zorros voladores al atardecer (Kalong)", "destino"),
    ("phinisi_boat", "Barco tradicional Phinisi en Komodo", "destino"),
    ("sidemen_rice", "Terrazas de arroz del Valle de Sidemen", "destino"),
    ("pura_kehen", "Pura Kehen, templo sagrado escalonado", "destino"),
    ("gunung_kawi", "Gunung Kawi, santuarios en acantilado", "destino"),
    ("banyumala", "Cascadas gemelas de Banyumala (Munduk)", "destino"),
    ("tamblingan", "Lago Tamblingan en canoa tradicional", "destino"),

    # 10 Alojamientos especiales, todos en la Ruta B (Sidemen, Komodo y Munduk)
    ("hotel_taaktana", "TA'AKTANA (Villas sobre el agua y espigón)", "hotel"),
    ("hotel_ayana", "AYANA Komodo (Espigón de 250m sobre el mar)", "hotel"),
    ("hotel_sudamala", "Sudamala Seraya (Bungalows en arena y arrecife)", "hotel"),
    ("hotel_plataran", "Plataran Komodo (Villas de madera y cala)", "hotel"),
    ("hotel_komodo_resort", "Komodo Resort Sebayur (Playa virgen y bungalows de teca)", "hotel"),
    ("hotel_wapa_diume", "Wapa di Ume Sidemen (Villa con piscina y vistas al Agung)", "hotel"),
    ("hotel_samanvaya", "Samanvaya Resort (Villa de bambú entre arrozales de Sidemen)", "hotel"),
    ("hotel_camaya_hideout", "Hideout / Camaya (Cabaña de bambú en río)", "hotel"),
    ("hotel_munduk_moding", "Munduk Moding (Piscina infinita en las nubes)", "hotel"),
    ("hotel_sanak_retreat", "Sanak Retreat (Bungalow de madera junto a Munduk)", "hotel"),
    ("amanjiwo", "Amanjiwo, suite con vistas a Borobudur (ultra lujo)", "hotel"),

    # Ampliación de contenidos: transporte, Java, Komodo, Bali y gastronomía
    ("zaragoza_delicias", "Tren AVE saliendo de Zaragoza Delicias", "destino"),
    ("changi_jewel", "Vórtice de agua y torre de control, Jewel Changi", "destino"),
    ("hamad_doha", "Interior del aeropuerto de Doha", "destino"),
    ("yogya_tamansari", "Taman Sari, el antiguo castillo de agua del sultán", "destino"),
    ("yogya_kraton", "Pabellón ceremonial del Kraton de Yogyakarta", "destino"),
    ("borobudur_relief", "Relieve tallado en piedra de Borobudur", "destino"),
    ("borobudur_setumbu", "Amanecer de niebla sobre Borobudur desde Punthuk Setumbu", "destino"),
    ("merapi", "El volcán Merapi sobre los arrozales de Java", "destino"),
    ("ramayana_ballet", "Ballet Ramayana frente a Prambanan", "destino"),
    ("ratu_boko", "Puerta de Ratu Boko al atardecer", "destino"),
    ("gudeg", "Gudeg, el plato tradicional de Yogyakarta", "destino"),
    ("labuan_bajo", "Atardecer sobre el puerto de Labuan Bajo", "destino"),
    ("kelor", "Restos del antiguo muelle de la Isla Kelor", "destino"),
    ("rinca", "Vista de la Isla Rinca desde el mirador", "destino"),
    ("kanawa", "Muelle de madera sobre aguas turquesa en Kanawa", "destino"),
    ("agung", "El monte Agung reflejado en los arrozales", "destino"),
    ("tirta_empul", "Fuentes sagradas de purificación de Tirta Empul", "destino"),
    ("pura_mengening", "Cascada sagrada de Pura Mengening", "destino"),
    ("canang_sari", "Ofrenda diaria canang sari", "destino"),
    ("penjor", "Penjor de bambú decorando un templo balinés", "destino"),
    ("munduk", "El pueblo de montaña de Munduk entre colinas verdes", "destino"),
    ("ulun_danu", "Templo Ulun Danu Bratan flotando sobre el lago", "destino"),
    ("menjangan_reef", "Buceador en el arrecife de Menjangan", "destino"),
    ("espigon_arrecife", "Espigón de madera sobre el arrecife (Kanawa, Komodo)", "destino"),
    ("babi_guling", "Babi guling, el cerdo asado ceremonial balinés", "destino"),
    ("nasi_campur", "Nasi campur, plato combinado balinés", "destino"),
    ("bebek_betutu", "Bebek betutu, pato especiado balinés", "destino"),
    ("sate_lilit", "Sate lilit, brochetas balinesas de pescado especiado", "destino"),
    ("kopi", "Mercado tradicional de café en Indonesia", "destino"),

    # Apoyo visual de las secciones de logistica y de criterio
    ("avion_sq", "Airbus A350 de Singapore Airlines en Changi", "destino"),
    ("gili_fiesta", "Noche de fiesta en Gili Trawangan (descartado)", "destino"),
    ("kelingking", "Kelingking Beach en Nusa Penida (descartado)", "destino"),
    ("kuta_comercial", "Centro comercial Beachwalk en Kuta (descartado)", "destino"),
]

cache = {}
saved_list = []

for key, label, cat in ITEMS:
    p = os.path.join(RAW_DIR, f"{key}.webp")
    if not os.path.exists(p):
        print(f"MISSING: {p}")
        continue
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    cache[key] = {
        "label": label,
        "cat": cat,
        "b64": f"data:image/webp;base64,{b64}"
    }
    saved_list.append((key, p, label, cat))

cache_path = os.path.join(BASE, "imgcache.json")
with open(cache_path, "w", encoding="utf-8") as f:
    json.dump(cache, f)

print(f"imgcache.json generado con {len(cache)} fotos ({os.path.getsize(cache_path)/1024/1024:.2f} MB)")

# Generar contact sheet
cols = 4
rows = (len(saved_list) + cols - 1) // cols
cw, ch = 320, 220
sheet = Image.new("RGB", (cols * cw, rows * ch), (24, 28, 36))
draw = ImageDraw.Draw(sheet)

for idx, (key, path, label, cat) in enumerate(saved_list):
    r = idx // cols
    c = idx % cols
    im = Image.open(path).resize((cw - 8, ch - 30), Image.Resampling.LANCZOS)
    sheet.paste(im, (c * cw + 4, r * ch + 4))
    tag = "[HOTEL]" if cat == "hotel" else "[DESTINO]"
    color = (255, 200, 100) if cat == "hotel" else (100, 220, 255)
    draw.text((c * cw + 6, r * ch + ch - 22), f"{tag} {label[:30]}", fill=color)

sheet_path = os.path.join(BASE, "hoja_contactos.jpg")
sheet.save(sheet_path, "JPEG", quality=85)
print(f"Hoja de contactos guardada en {sheet_path}")
