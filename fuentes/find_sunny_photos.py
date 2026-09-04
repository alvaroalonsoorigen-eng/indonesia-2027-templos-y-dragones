import urllib.request, urllib.parse, json, re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_bing_urls(q, n=3):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(q)}&form=HDRSC2&first=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
        murls = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        return murls[:n]
    except Exception as e:
        print(f"Error {q}: {e}")
        return []

targets = [
    "luxury phinisi boat komodo turquoise water",
    "Komodo Resort Sebayur island beach bungalow sunny",
    "AYANA Komodo Waecicu Beach pier sunset kisik bar",
    "TA'AKTANA Labuan Bajo overwater villa sunny",
    "Plataran Komodo Waecicu beach villas sunny"
]

for t in targets:
    res = get_bing_urls(t, 2)
    print(f"=== {t} ===")
    for u in res:
        print("  ", u)
