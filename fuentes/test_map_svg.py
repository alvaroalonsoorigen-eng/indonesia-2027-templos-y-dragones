import urllib.request, json, math, os

url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as r:
    gj = json.loads(r.read().decode())

target_provinces = {
    "Jakarta Raya", "Banten", "Jawa Barat", "Jawa Tengah", "Yogyakarta", 
    "Jawa Timur", "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur"
}

# Coordinate bounding box for Java + Bali + Lombok + Sumbawa + Flores/Komodo
# Lon: 105.0 to 121.0
# Lat: -5.6 to -9.2
W, H = 1000.0, 360.0
LON_MIN, LON_MAX = 105.0, 121.0
LAT_MAX, LAT_MIN = -5.4, -9.3  # Y grows downwards in SVG: higher lat (-5.4) -> top, lower lat (-9.3) -> bottom

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
    gtype = geom.get("type")
    coords = geom.get("coordinates", [])
    if gtype == "Polygon":
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
print(f"Generated land SVG path with {len(paths)} polygons, string size: {len(svg_land)/1024:.1f} KB")

# Test key city coordinates
places = {
    "Yakarta": (106.84, -6.20),
    "Borobudur": (110.20, -7.60),
    "Prambanan": (110.49, -7.75),
    "Sidemen": (115.45, -8.48),
    "Munduk": (115.06, -8.27),
    "Labuan Bajo": (119.88, -8.49),
    "Komodo": (119.60, -8.60),
}
for name, (lo, la) in places.items():
    print(f"  {name:12}: {proj(lo, la)}")
