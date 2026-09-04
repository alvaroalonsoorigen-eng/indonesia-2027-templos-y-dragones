#!/usr/bin/env python3
"""
Generador del index.html para Indonesia 2027:
- EN ORDENADOR:
  - Layout en dos columnas estilo China 2027: columna izquierda con los 14 dias individuales y columna derecha pegajosa (sticky) con el mapa interactivo.
  - Sincronizacion dinamica con scroll: conforme el usuario baja por los dias, los tramos se van uniendo e iluminando secuencialmente (done / now), la baliza beacon se traslada a la isla/ciudad activa, la barra de progreso avanza y el titulo del mapa cambia en tiempo real.
- EN MOVIL:
  - Arquitectura tipo app nativa por secciones / pantallas independientes (Vistas: Ruta, Mapa, Hoteles, Vuelos, Criterio) activadas por la barra inferior (.bottomnav).
  - Mejora radical de rendimiento y velocidad de carga en movil: evita renderizado simultaneo pesado y desplazamiento interminable.
- Paleta oficial Sarah Renae Clark clara, tipografia DM Serif Display + Plus Jakarta Sans, fotos limpias y cero rayas largas.
"""
import os, json, sys

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE, "imgcache.json")
LAND_FILE = os.path.join(BASE, "mapa_land.json")
OUTPUT_FILE = os.path.join(os.path.dirname(BASE), "index.html")

if not os.path.exists(CACHE_FILE) or not os.path.exists(LAND_FILE):
    print("Error: archivos necesarios no encontrados.")
    sys.exit(1)

with open(CACHE_FILE, "r", encoding="utf-8") as f:
    IMG = json.load(f)

with open(LAND_FILE, "r", encoding="utf-8") as f:
    LAND_DATA = json.load(f)

svg_land_path = LAND_DATA["land_svg"]

def get_img(k):
    return IMG.get(k, {}).get("b64", "")

# Let's construct the full HTML
print("Generando HTML...")
