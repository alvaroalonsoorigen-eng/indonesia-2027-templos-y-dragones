# Indonesia 2027: entre templos y dragones

Documento de decisión interactivo para un viaje de 14 días por Indonesia, del 21 de abril al 4 de mayo de 2027, con dos rutas alternativas para comparar y elegir.

**[Abrir el documento](https://alvaroalonsoorigen-eng.github.io/indonesia-2027-templos-y-dragones/)**

## Qué es

Una sola página HTML autocontenida, de unos 8,5 MB, que funciona **sin conexión y sin servidor**: basta abrir `index.html` en cualquier navegador. Todas las fotos, el vídeo de portada, las tipografías y el mapa van embebidos en el propio fichero (WebP y WOFF2 en base64, y SVG vectorial), sin una sola llamada de red ni dependencia externa.

## Contenido

- **Dos rutas de 14 días comparables.** Ruta A con Java (Borobudur y Prambanan); Ruta B sin Java, con más tiempo en Bali. Se conmutan con un botón y el mapa se resincroniza.
- **Los 28 días descritos uno a uno**, con franjas horarias, y mapa que avanza solo al hacer scroll.
- **Colección de 10 alojamientos**, todos sobre la ruta, con enlace desde el día que corresponde.
- **Cronología de Indonesia en 30 hitos**, filtrable por era, del Homo erectus de Java a la actualidad.
- **Guía práctica**: visado, salud, dinero, conectividad, clima, equipaje.
- **Logística aérea y criterio de descartes**, con el razonamiento de por qué se descartan destinos populares.

## Criterio de exactitud

El documento distingue de forma explícita lo verificado de lo que no lo está:

- Cuando las fuentes discrepan (tasas de parques, requisito de visado, riesgo de malaria), **se muestra la discrepancia** en lugar de elegir una versión arbitrariamente.
- Los hitos históricos en discusión entre especialistas **llevan un aviso visible**; no se presenta como cerrado lo que la investigación mantiene abierto.
- Los datos que no se pudieron confirmar **se dejan señalados como huecos**, no rellenados con cifras plausibles.
- Todas las fotografías son **reales y verificadas una a una**, de Wikimedia Commons con licencia libre o de galerías oficiales de los establecimientos. No hay banco de imágenes ni fotos generadas.

## Cómo se regenera

`index.html` **no se edita a mano**: es la salida de un generador.

```bash
cd fuentes
python3 build_cache.py   # procesa las fotos de raw/ y genera imgcache.json
python3 build.py         # genera ../index.html
```

Requiere Python 3 y Pillow. `build.py` valida al terminar que no se haya colado ninguna raya larga y que el mapa quede sincronizado.

### Estructura

```
├── index.html              Documento final (generado, no editar)
├── progress.md             Registro de decisiones de diseño y peticiones resueltas
└── fuentes/
    ├── build.py            Generador principal
    ├── build_cache.py      Empaqueta las fotos a base64
    ├── imgcache.json       Las 54 fotos en WebP base64
    ├── hero_loop.mp4       Vídeo de portada (20 s en bucle)
    ├── mapa_land.json      Polígonos de la costa de Indonesia
    ├── hoja_contactos.jpg  Mosaico para verificar las fotos a ojo
    ├── *.woff2             Tipografías autoalojadas
    └── raw/                Fotos individuales en WebP
```

## Créditos fotográficos

Las imágenes provienen de **Wikimedia Commons** (licencias CC BY-SA, con autoría recogida en `progress.md`) y de las **galerías oficiales** de los alojamientos citados, que conservan sus derechos. El vídeo de portada se montó a partir de seis fotografías de Wikimedia Commons con licencia libre.
