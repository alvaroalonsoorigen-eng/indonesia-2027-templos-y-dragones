import urllib.request, json, os

url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as r:
    gj = json.loads(r.read().decode())

target_provinces = {
    "Jakarta Raya", "Banten", "Jawa Barat", "Jawa Tengah", "Yogyakarta", 
    "Jawa Timur", "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur"
}

W, H = 1000.0, 420.0
LON_MIN, LON_MAX = 105.0, 120.8
LAT_MAX, LAT_MIN = -5.5, -9.1

def proj(lon, lat):
    x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * W
    y = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * H
    return round(x, 1), round(y, 1)

paths = []
for f in gj["features"]:
    name = f.get("properties", {}).get("state")
    if name not in target_provinces:
        continue
    geom = f.get("geometry", {})
    coords = geom.get("coordinates", [])
    if geom.get("type") == "Polygon":
        coords = [coords]
    for poly in coords:
        ring = poly[0]
        pts = []
        for pt in ring:
            lo, la = pt[0], pt[1]
            if 104.5 <= lo <= 121.5 and -10.0 <= la <= -5.0:
                px, py = proj(lo, la)
                if not pts or (abs(px - pts[-1][0]) + abs(py - pts[-1][1]) > 1.2):
                    pts.append((px, py))
        if len(pts) >= 4:
            d = "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
            paths.append(d)

svg_land = " ".join(paths)
out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapa_land.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({"land_svg": svg_land}, f)

print(f"mapa_land.json guardado: {os.path.getsize(out_file)/1024:.1f} KB")
