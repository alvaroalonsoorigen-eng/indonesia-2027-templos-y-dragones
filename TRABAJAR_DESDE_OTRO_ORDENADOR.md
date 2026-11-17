# Indonesia 2027: cómo seguir trabajando desde otro ordenador

Guía completa para retomar el proyecto en cualquier equipo. Actualizada el 18 de noviembre de 2026.

## 1. Enlaces

- **Web publicada (la que se comparte):** https://alvaroalonsoorigen-eng.github.io/indonesia-2027-templos-y-dragones/
- **Repositorio en GitHub (código y fuentes):** https://github.com/alvaroalonsoorigen-eng/indonesia-2027-templos-y-dragones
- **Cuenta de GitHub:** `alvaroalonsoorigen-eng`
- **Carpeta en el Mac principal:** `~/Desktop/ALVARO/04 PERSONAL/Viajes/Indonesia 2027 - Templos y dragones`

La web se publica sola con GitHub Pages: cada vez que se sube un cambio a la rama `main`, en uno o dos minutos la web queda actualizada en el mismo enlace.

## 2. Qué es el proyecto

Documento de decisión interactivo para el viaje del 21 de abril al 4 de mayo de 2027, con dos rutas de 14 días para comparar:

- **Ruta A (con Java):** Yogyakarta (Borobudur y Prambanan), Komodo en barco y resort con espigón, y Bali rural (Sidemen).
- **Ruta B (sin Java):** Sidemen, Komodo, y el norte de Bali (Munduk y cascadas).

Incluye mapa que avanza con el scroll, 10 alojamientos, cronología de Indonesia en 30 hitos, guía práctica (visado, salud, dinero, clima), logística aérea, criterio de descartes y paisajes animados.

Es **una sola página HTML de unos 8 MB que funciona sin conexión**: fotos, vídeo de portada, tipografías y mapa van dentro del propio fichero.

## 3. Estado actual

- Último cambio: 18 de noviembre de 2026. Se eliminaron fotos duplicadas dentro del HTML: de 9,49 a 8,03 MB, sin perder calidad.
- Web publicada idéntica a la versión local, verificada.
- Pendiente según el registro: precios de vuelos (se abren unos 11 meses antes), y reconfirmar visado, tasas de parques y salud 2 o 3 meses antes de volar.
- Todo el historial de decisiones está en `progress.md`.

## 4. Preparar el otro ordenador (una sola vez)

Hace falta **Git**, **Python 3** y la librería de imágenes **Pillow**.

1. Instalar Git y Python 3 si no están (en Mac, `git --version` ofrece instalarlos; en Windows, desde git-scm.com y python.org).
2. Descargar el proyecto:

```bash
git clone https://github.com/alvaroalonsoorigen-eng/indonesia-2027-templos-y-dragones.git
```

3. Instalar Pillow:

```bash
python3 -m pip install pillow
```

4. Configurar la identidad de Git solo para este proyecto, con el correo privado de GitHub para no exponer el real en un repositorio público:

```bash
cd indonesia-2027-templos-y-dragones
git config user.name "alvaroalonsoorigen-eng"
git config user.email "242413540+alvaroalonsoorigen-eng@users.noreply.github.com"
```

5. Para poder subir cambios hay que iniciar sesión en GitHub en ese equipo. Lo más sencillo es GitHub CLI (`gh auth login`) o GitHub Desktop. Git pedirá la sesión la primera vez que se suba algo.

## 5. Cómo hacer un cambio

**Regla clave: `index.html` no se edita a mano.** Es la salida de un generador. Los textos, rutas, hoteles y guía viven en `fuentes/build.py`.

1. Traer la última versión antes de empezar:

```bash
git pull
```

2. Editar lo que corresponda:
   - Textos, días, hoteles, guía, cronología: `fuentes/build.py`
   - Paisajes animados del scroll: `fuentes/scroll-scenes.html`, `fuentes/scroll-motion.css`, `fuentes/scroll-motion.js`
   - Fotos: añadir el WebP en `fuentes/raw/`, darlo de alta en la lista `ITEMS` de `fuentes/build_cache.py` y usarlo en `build.py` con `get_img("nombre")`

3. Si se han tocado fotos, regenerar primero la caché:

```bash
cd fuentes
python3 build_cache.py
```

4. Regenerar la web:

```bash
cd fuentes
python3 build.py
```

El generador se detiene si encuentra una raya larga, e incrusta una sola vez las fotos repetidas.

5. Revisar abriendo `index.html` en el navegador (doble clic; funciona sin servidor).

6. Subir y publicar:

```bash
git add -A
git commit -m "Descripción breve del cambio"
git push
```

En uno o dos minutos la web publicada se actualiza en el mismo enlace.

## 6. Trabajar con un agente de IA (Claude Code, Cursor, Antigravity)

Abrir la carpeta del proyecto y pedirle que lea primero `AGENTS.md`, `README.md` y el final de `progress.md`. Ahí están las reglas y el contexto completo.

Reglas del proyecto que el agente debe respetar:

1. Todo en español.
2. Nunca rayas largas en ningún texto: usar coma, dos puntos o paréntesis.
3. Mayúsculas a la española en títulos: solo la primera palabra y nombres propios.
4. Solo fotos reales y verificadas, nunca de banco ni generadas.
5. No tocar otros proyectos de viajes: este es independiente.
6. Preguntar antes de subir a GitHub.
7. Registrar cada cambio en `progress.md` para poder retomar desde cualquier sesión.

## 7. Estructura de la carpeta

```
├── index.html                  Web final (generada, no editar)
├── README.md                   Presentación del proyecto
├── AGENTS.md                   Instrucciones para agentes de IA
├── progress.md                 Registro de decisiones y cambios
├── TRABAJAR_DESDE_OTRO_ORDENADOR.md   Esta guía
└── fuentes/
    ├── build.py                Generador principal (contenido de la web)
    ├── build_cache.py          Empaqueta las fotos en imgcache.json
    ├── imgcache.json           Las 58 fotos en WebP base64
    ├── raw/                    Fotos individuales en WebP (900 x 580)
    ├── hero_loop.mp4           Vídeo de portada
    ├── mapa_land.json          Costa de Indonesia para el mapa
    ├── scroll-scenes.html      Paisajes animados (Java, Komodo, Bali)
    ├── scroll-motion.css / .js Movimiento con el scroll
    ├── hoja_contactos.jpg      Mosaico para revisar todas las fotos
    └── *.woff2                 Tipografías
```

## 8. Si algo falla

- **`git push` pide usuario y contraseña:** GitHub ya no acepta contraseña; usar `gh auth login` o GitHub Desktop.
- **`No module named PIL`:** falta Pillow, ver el paso 3 del apartado 4.
- **`ERROR CRITICO: raya larga`:** hay un guion largo en algún texto de `build.py`; sustituirlo.
- **La web publicada no cambia:** esperar dos minutos y recargar forzando (Cmd+Shift+R en Mac, Ctrl+F5 en Windows).
- **Conflicto al hacer `git pull`:** se ha cambiado lo mismo en dos ordenadores; resolver en `build.py` y volver a generar `index.html`, nunca mezclar `index.html` a mano.
