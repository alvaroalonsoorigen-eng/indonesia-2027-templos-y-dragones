import urllib.request, urllib.parse, json, time

API = "https://commons.wikimedia.org/w/api.php"
UA = "IndonesiaTripPlanner/3.0 (personal travel planner; alvaroalonso)"

def search_commons(query, limit=5):
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "iiurlwidth": "1280"
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.loads(r.read().decode())
            pages = d.get("query", {}).get("pages", [])
            res = []
            for p in pages:
                title = p.get("title", "")
                if any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                    ii = (p.get("imageinfo") or [{}])[0]
                    thumb = ii.get("thumburl") or ii.get("url")
                    orig = ii.get("url")
                    w = ii.get("width", 0)
                    h = ii.get("height", 0)
                    res.append((title, thumb, w, h))
            return res
        except Exception as e:
            time.sleep(2 + intento * 2)
    return []

for q in ["Borobudur sunrise stupa", "Phinisi Komodo boat", "Kalong Island sunset", "Padar Island turquoise"]:
    res = search_commons(q, 3)
    print(f"=== {q} ===")
    for t, u, w, h in res:
        print(f"  {t} ({w}x{h})")
