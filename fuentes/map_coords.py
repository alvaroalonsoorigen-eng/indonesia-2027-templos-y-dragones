import json, math, os

# Let's generate the SVG land path and route coordinates
# Bounding box: Lon 105.0 to 120.8, Lat -5.5 to -9.1
W, H = 1000.0, 420.0
LON_MIN, LON_MAX = 105.0, 120.8
LAT_MAX, LAT_MIN = -5.5, -9.1

def proj(lon, lat):
    x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * W
    y = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * H
    return round(x, 1), round(y, 1)

def arc(p1, p2, bend=-0.15):
    x1, y1 = p1
    x2, y2 = p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx = round(mx - dy * bend, 1)
    cy = round(my + dx * bend, 1)
    return f"M {x1} {y1} Q {cx} {cy} {x2} {y2}"

# Nodes
NODES = {
    "es": {"name": "Zaragoza / España", "pos": (40.0, 50.0), "type": "origin"},
    "cgk": {"name": "Yakarta", "coord": (106.84, -6.20)},
    "yia": {"name": "Borobudur / Yogyakarta", "coord": (110.36, -7.79)},
    "dps": {"name": "Denpasar (Bali)", "coord": (115.16, -8.74)},
    "sidemen": {"name": "Valle de Sidemen", "coord": (115.45, -8.48)},
    "munduk": {"name": "Munduk / Banyumala", "coord": (115.06, -8.27)},
    "lbj": {"name": "Labuan Bajo (Flores)", "coord": (119.88, -8.49)},
    "komodo": {"name": "P.N. Komodo / Padar / Mantas", "coord": (119.58, -8.65)},
    "resort": {"name": "Resort Isla Sebayur / Seraya", "coord": (119.72, -8.52)}
}

for k, v in NODES.items():
    if "coord" in v:
        v["pos"] = proj(v["coord"][0], v["coord"][1])
    print(f"Node {k:10}: {v['pos']} ({v['name']})")
