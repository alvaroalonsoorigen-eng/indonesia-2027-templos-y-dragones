# AGENTS.md · Indonesia 2027, entre templos y dragones

Instrucciones para el agente que abra esta carpeta (Antigravity, Claude Code, Cursor o cualquier otro). Léelas enteras antes de tocar nada.

---

## 1. Qué es esto

Un **documento de decisión** interactivo de viaje para dos personas de 32 años muy activas, centrado en naturaleza salvaje, snorkel, cultura ancestral y desconexión en alojamientos únicos sobre el mar o playas privadas.

Compara dos rutas para las fechas exactas del 21 de abril al 4 de mayo (11 noches netas en destino, con salida y regreso cerrados en Zaragoza):
- **Ruta A (Con Java):** Yogyakarta (Borobudur y Prambanan) + Komodo (barco tradicional Phinisi y resort de espigón) + Bali rural (Sidemen).
- **Ruta B (Sin Java):** Bali sagrado (Sidemen y templos de roca) + Komodo (barco y resort) + Norte místico (Munduk y cascadas).

El entregable es **un único `index.html` autónomo de menos de 3 MB que funciona 100% sin conexión**: 26 fotos reales verificadas a ojo (destinos y 12 alojamientos) van incrustadas en base64 WebP. Sin CDN, sin librerías externas que requieran internet, sin llamadas a red.

---

## 2. Reglas obligatorias de Álvaro

1. **Responde en español.**
2. **Nunca uses la raya larga** en ningún texto: ni en las webs, ni en los commits, ni en los mensajes. Usa coma, punto, dos puntos o reformula.
3. **Mayúsculas a la española** en los títulos: solo la primera palabra y los nombres propios.
4. **Fotos reales verificadas a ojo.** Nada de stock. Cada foto está revisada en `fuentes/hoja_contactos.jpg`.
5. **No toques otros proyectos de la colección.** Este proyecto es totalmente independiente.
6. **Pregunta antes de subir a GitHub.** Tras cada cambio local, consulta si se desea crear repositorio remoto o subir cambios.

---

## 3. Estructura de la carpeta

```
Indonesia 2027 - Templos y dragones/
├── index.html                      <- ARCHIVO GENERADO. Documento de decisión interactivo.
├── AGENTS.md                       <- Este archivo de instrucciones.
└── fuentes/
    ├── build.py                    <- Monta index.html inyectando imgcache.json.
    ├── build_cache.py              <- Genera imgcache.json y la hoja de contactos.
    ├── imgcache.json               <- Las 26 fotos codificadas en base64 WebP.
    ├── hoja_contactos.jpg          <- Mosaico de comprobación visual de todas las fotos.
    ├── raw/                        <- Fotos individuales procesadas en WebP (800x520).
    └── descargar_y_procesar.py     <- Script de descarga original de imágenes.
```

---

## 4. Cómo reconstruir

Para regenerar el `index.html`:

```bash
cd "fuentes"
python3 build.py
```

El script valida automáticamente que no existan rayas largas antes de escribir el archivo de salida.

---

## 5. Cómo verificar localmente

Por restricciones de permisos de macOS sobre carpetas de escritorio con espacios, copia el archivo a `/tmp` para servirlo:

```bash
mkdir -p /tmp/viaje && cp index.html /tmp/viaje/ && cd /tmp/viaje && python3 -m http.server 8901
```

Abre `http://localhost:8901/` en el navegador para comprobar:
- Alternancia instantánea entre la Ruta A (con Java) y la Ruta B (sin Java).
- Filtrado por categorías de la sección de 12 alojamientos especiales (espigón, playa privada, bambú).
- Carga nítida e instantánea de las 26 fotografías sin conexión a internet.
